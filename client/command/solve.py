from dataclasses import asdict
from difflib import unified_diff
from json import dumps
from os import remove
from os.path import exists
from time import sleep
from typing import List, Tuple

from click import argument, command, echo, secho, prompt
from requests import post, Response
from simplejson.errors import JSONDecodeError

from ..config import config
from ..helper.api_key import load_api_key, APIKeyMissing
from ..helper.error_messages import error_messages
from ..helper.files import write
from ..model.task import markdown_to_task, MissingDataError, Place, Task, \
    json_to_places_list


class ServerError(Exception):
    pass


@command()
@argument("file_path", default="task.md")
def solve(file_path: str = "task.md"):
    """Solve a programming task given a task description

    \b
    Args:
        file_path(str): Path to task file. Default: "task.md".
    """
    task = None
    changes = None

    try_again = True
    while try_again:
        try:
            task = markdown_to_task(file_path)
            echo('Solving task "' + file_path + '"...')
            changes = send_request_to_solve(task)
            display_changes(task.places_to_change, changes)
        except handled_errors() as error:
            echo(error_messages[str(error)])

        try_again = ask("Try again?")
        if try_again:
            echo("Let's try again...")
            continue

        if not changes:
            return

        apply = ask("Apply changes?")
        if not apply:
            continue
        apply_changes(task.places_to_change, changes)

        echo("You can test the changes now.")
        revert = ask("Revert changes?")
        if revert:
            apply_changes(changes, task.places_to_change)
            try_again = ask("Try again?")


class ServerTimeoutError(ServerError):
    pass


def send_request_to_solve(task: Task, attempt: int = 1) -> List[Place]:
    response = post(
        config['SOLVE_ENDPOINT'],
        json=dumps({"task": asdict(task), "allow_cached": attempt != 1}),
        headers={"X-API-KEY": load_api_key()}
    )
    try:
        validate_response(response)
    except ServerTimeoutError as error:
        if attempt < 4:
            echo("Still waiting for the response...")
            sleep(15)
            return send_request_to_solve(task, attempt + 1)
        raise error
    return json_to_places_list(response.json())


def validate_response(response: Response):
    if response.status_code == 503:
        raise ServerTimeoutError("Timeout")
    if response.status_code == 404:
        raise ServerError("Server not found")
    try:
        body = response.json()
    except JSONDecodeError:
        raise ServerError("Unexpected error")
    if response.status_code != 200:
        raise ServerError(body['error'])


def display_changes(places_to_change: List[Place], changes: List[Place]):
    if places_to_change == changes:
        echo("Acoder hasn't produced any change in the files.")
        return
    long_text = False
    for place, change in zip(places_to_change, changes):
        difference = unified_diff(
            place.code.splitlines(),
            change.code.splitlines(),
            fromfile=place.file_path,
            tofile=change.file_path
        )
        for line in difference:
            if line.startswith("+"):
                secho(line, fg="green")
            elif line.startswith("-"):
                secho(line, fg="red")
            else:
                echo(line)
            if "{long_text}" in line:
                long_text = True
    if long_text:
        echo("Part of the output has been filtered out.")


def handled_errors() -> Tuple:
    return APIKeyMissing, FileNotFoundError, MissingDataError, ServerError


def ask(prompt_: str):
    answer = prompt(prompt_ + " (y/n)").lower() == "y"
    echo("")
    return answer


def apply_changes(old: List[Place], new: List[Place]):
    for old_place, new_place in zip(old, new):
        if new_place.code == "":
            if exists(new_place.file_path):
                remove(new_place.file_path)
            continue
        write(new_place.file_path, new_place.code)
