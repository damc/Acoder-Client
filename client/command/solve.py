from difflib import unified_diff
from os import remove
from typing import List

from click import argument, command, echo, prompt
from requests import post

from ..config import config
from ..helper.api_key import load_api_key
from ..helper.files import write
from ..model.task import markdown_to_task, Place, Task, task_to_json


@command()
@argument("file_path", default="task.md")
def solve(file_path: str):
    """Solve the task from the task description

    args:
        file_path(str): Path to task file
    """
    try_again = True
    while try_again:
        task = markdown_to_task(file_path)

        echo('Solving task "' + file_path + '"...')
        changes = send_request_to_solve(task)

        display_changes(task.places_to_change, changes)

        try_again = ask("Try again?")
        if try_again:
            continue

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
    changes = response.json()
    for key, change in enumerate(changes):
        changes[key] = Place(**change)
    return changes


def display_changes(places_to_change: List[Place], changes: List[Place]):
    any_changes = False
    for place, change in zip(places_to_change, changes):
        if place.code != change.code:
            any_changes = True
        differences = unified_diff(
            place.code.splitlines(),
            change.code.splitlines(),
            fromfile=place.file_path,
            tofile=change.file_path
        )
        for line in differences:
            echo(line)
    if not any_changes:
        echo("Acoder hasn't produced any change in the files.")


def ask(prompt_: str):
    return prompt(prompt_ + " (y/n)").lower() == "y"


def apply_changes(old: List[Place], new: List[Place]):
    for old_place, new_place in zip(old, new):
        if new_place.code == "":
            remove(new_place.file_path)
            continue
        write(new_place.file_path, new_place.code)
