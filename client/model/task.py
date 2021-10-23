from dataclasses import dataclass, asdict
from json import dumps
from typing import List, Optional

from ..helper.files import content
from ..helper.markdown import load_markdown


@dataclass
class Place:
    file_path: str
    functions: Optional[List[str]]
    code: Optional[str]


@dataclass
class Task:
    title: str
    description: str
    places_to_change: List[Place]
    places_to_look: List[Place]


class MissingDataError(Exception):
    pass


def markdown_to_task(file_path: str) -> Task:
    data = load_markdown(file_path)
    if "description" not in data:
        raise MissingDataError("Task file missing description")
    if "change" not in data:
        raise MissingDataError("Task file missing change")
    change_lines = data['change'].splitlines()
    change = [line_to_place(line, True) for line in change_lines]
    look = []
    if "look" in data and data["look"] != "":
        look_lines = data['look'].splitlines()
        look = [line_to_place(line, False) for line in look_lines]
    return Task(data['title'], data['description'], change, look)


def line_to_place(line: str, allow_new_files: bool) -> Place:
    split = line.split('->')
    file_path = split[0]
    file_path = file_path.strip()
    functions = None
    if len(split) > 1:
        functions = split[1]
        functions = functions.split(',')
        functions = [function.strip() for function in functions]
    code = retrieve_code(file_path, functions, allow_new_files)
    return Place(file_path, functions, code)


def retrieve_code(
        file_path: str,
        functions: List[str],
        allow_new_files: bool
) -> str:
    code = content(file_path, "" if allow_new_files else None)
    if functions:
        raise NotImplementedError("Functions not implemented")
    return code


def task_to_json(task):
    return dumps(asdict(task))


def json_to_places_list(changes) -> List[Place]:
    for key, change in enumerate(changes):
        changes[key] = Place(**change)
    return changes