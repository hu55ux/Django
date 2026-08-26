from copy import deepcopy
from typing import Any

from typing import Any

_NOTES: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Django Views",
        "body": "Views accept a request and return a response.",
        "tag": "django",
        "category": "backend"
    },
    {
        "id": 2,
        "title": "Django Models",
        "body": "Models are used to define the structure of database tables.",
        "tag": "django",
        "category": "database"
    },
    {
        "id": 3,
        "title": "Django Templates",
        "body": "Templates are used to generate dynamic HTML pages.",
        "tag": "django",
        "category": "frontend"
    },
    {
        "id": 4,
        "title": "Django URLs",
        "body": "URL patterns connect URLs to corresponding views.",
        "tag": "django",
        "category": "backend"
    },
    {
        "id": 5,
        "title": "Django ORM",
        "body": "Django ORM allows developers to work with databases using Python objects.",
        "tag": "django",
        "category": "database"
    },
    {
        "id": 6,
        "title": "Django Forms",
        "body": "Forms are used to receive and validate data submitted by users.",
        "tag": "django",
        "category": "backend"
    },
    {
        "id": 7,
        "title": "HTTP Request",
        "body": "An HTTP request is sent by a client to request a resource from a server.",
        "tag": "http",
        "category": "web"
    },
    {
        "id": 8,
        "title": "HTTP Response",
        "body": "An HTTP response is returned by a server after processing a request.",
        "tag": "http",
        "category": "web"
    },
    {
        "id": 9,
        "title": "Python Functions",
        "body": "Functions are reusable blocks of code that perform a specific task.",
        "tag": "python",
        "category": "programming"
    },
    {
        "id": 10,
        "title": "Python Classes",
        "body": "Classes are blueprints used to create objects with attributes and methods.",
        "tag": "python",
        "category": "programming"
    },
]

_next_id = 11

def list_notes()->list[dict[str, Any]]:
    return deepcopy(_NOTES)


def get_note(note_id:int)-> dict[str, Any] | None:
    for note in _NOTES:
        if note["id"] == note_id:
            return deepcopy(note)
    return None


def create_note(*, title:str, body:str, tag:str, category:str)-> dict[str, Any]:
    global _next_id
    note = {
        "id": _next_id,
        "title": title.strip(),
        "body": body.strip(),
        "tag": tag.strip(),
        "category": category.strip()
    }
    _NOTES.append(note)
    _next_id += 1
    return deepcopy(note)


def update_note(
        note_id:int,
        *,
        title:str,
        body:str,
        tag:str,
        category:str,
)-> dict[str, Any] | None:
    for note in _NOTES:
        if note["id"] == note_id:
            note["title"] = title.strip()
            note["body"] = body.strip()
            note["category"] = category.strip()
            note["tag"] = tag.strip()
            return deepcopy(note)
    return None


def delete_note(note_id:int)-> bool:
    global _NOTES
    before = len(_NOTES)
    _NOTES = [n for n in _NOTES if n["id"] != note_id]
    return len(_NOTES) != before