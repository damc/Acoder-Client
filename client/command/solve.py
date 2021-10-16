from difflib import unified_diff
from os import remove
from os.path import exists
from typing import List

from click import argument, command, echo, prompt
from requests import post

from ..config import config
from ..helper.api_key import load_api_key
from ..helper.error_messages import error_messages
from ..helper.files import write
from ..model.task import markdown_to_task, MissingDataError, Place, Task, \
    task_to_json


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
    try_again = True
    while try_again:
        task = None
        changes = None
        try:
            task = markdown_to_task(file_path)
            echo('Solving task "' + file_path + '"...')
            changes = send_request_to_solve(task)
            display_changes(task.places_to_change, changes)
        except (FileNotFoundError, MissingDataError, ServerError) as error:
            echo(error_messages[str(error)])

        try_again = ask("Try again?")
        if try_again:
            continue

        if not changes:
            return

        apply = ask("Apply changes?")
        if not apply:
            continue
        apply_changes(task.places_to_change, changes)

        echo("It's time to test the changes.")
        revert = ask("Revert changes?")
        if revert:
            apply_changes(changes, task.places_to_change)
            try_again = ask("Try again?")


def send_request_to_solve(task: Task) -> List[Place]:
    api_key = load_api_key()
    response = post(
        config['SOLVE_ENDPOINT'],
        json=task_to_json(task),
        headers={"X-API-KEY": api_key}
    )
    if response.status_code == 404:
        raise ServerError("Server not found")
    if response.status_code != 200:
        raise ServerError(response.json()['error'])
    changes = response.json()
    for key, change in enumerate(changes):
        changes[key] = Place(**change)
    return changes


def display_changes(places_to_change: List[Place], changes: List[Place]):
    any_changes = False
    for place, change in zip(places_to_change, changes):
        if place.code != change.code:
            any_changes = True
        difference = unified_diff(
            place.code.splitlines(),
            change.code.splitlines(),
            fromfile=place.file_path,
            tofile=change.file_path
        )
        for line in difference:
            echo(line)
    if not any_changes:
        echo("Acoder hasn't produced any change in the files.")


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
