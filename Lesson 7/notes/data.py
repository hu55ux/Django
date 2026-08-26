from copy import deepcopy
from datetime import datetime
from typing import Any

_NOTES: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Django Views",
        "body": "Views accept a request and return a response.",
        "content": "Views accept a request and return a response.",
        "tag": "django",
        "tags": ["python", "django"],
        "category": "backend",
        "created_at": datetime(2026, 8, 24),
    },
    {
        "id": 2,
        "title": "Django Models",
        "body": "Models are used to work with data and databases.",
        "content": "Models are used to work with data and databases.",
        "tag": "django",
        "tags": ["python", "django", "database"],
        "category": "database",
        "created_at": datetime(2026, 8, 23),
    },
    {
        "id": 3,
        "title": "Django Templates",
        "body": "Templates are used to generate dynamic HTML pages.",
        "content": "Templates are used to generate dynamic HTML pages.",
        "tag": "django",
        "tags": ["django", "html"],
        "category": "frontend",
        "created_at": datetime(2026, 8, 22),
    },
    {
        "id": 4,
        "title": "Django URLs",
        "body": "URL patterns connect URLs with Django views.",
        "content": "URL patterns connect URLs with Django views.",
        "tag": "django",
        "tags": ["python", "django", "routing"],
        "category": "backend",
        "created_at": datetime(2026, 8, 21),
    },
    {
        "id": 5,
        "title": "Python Functions",
        "body": "Functions allow us to organize and reuse code.",
        "content": "Functions allow us to organize and reuse code.",
        "tag": "python",
        "tags": ["python", "functions"],
        "category": "programming",
        "created_at": datetime(2026, 8, 20),
    },
    {
        "id": 6,
        "title": "HTML Forms",
        "body": "HTML forms are used to collect data from users.",
        "content": "HTML forms are used to collect data from users.",
        "tag": "html",
        "tags": ["html", "forms"],
        "category": "frontend",
        "created_at": datetime(2026, 8, 19),
    },
    {
        "id": 7,
        "title": "Django Forms",
        "body": "Django Forms simplify validation and processing of user input.",
        "content": "Django Forms simplify validation and processing of user input.",
        "tag": "django",
        "tags": ["python", "django", "forms"],
        "category": "backend",
        "created_at": datetime(2026, 8, 18),
    },
    {
        "id": 8,
        "title": "CSS Basics",
        "body": "CSS is used to style HTML elements.",
        "content": "CSS is used to style HTML elements.",
        "tag": "css",
        "tags": ["css", "html"],
        "category": "frontend",
        "created_at": datetime(2026, 8, 17),
    },
    {
        "id": 9,
        "title": "Django Static Files",
        "body": "Static files include CSS, JavaScript, images, and other assets.",
        "content": "Static files include CSS, JavaScript, images, and other assets.",
        "tag": "django",
        "tags": ["django", "css", "javascript"],
        "category": "frontend",
        "created_at": datetime(2026, 8, 16),
    },
    {
        "id": 10,
        "title": "Django Middleware",
        "body": "Middleware processes requests and responses globally.",
        "content": "Middleware processes requests and responses globally.",
        "tag": "django",
        "tags": ["python", "django", "middleware"],
        "category": "backend",
        "created_at": datetime(2026, 8, 15),
    },
]

_next_id = 11


def list_notes() -> list[dict[str, Any]]:
    return deepcopy(_NOTES)


def get_note(note_id: int) -> dict[str, Any] | None:
    for note in _NOTES:
        if note["id"] == note_id:
            return deepcopy(note)
    return None


def create_note(*, title: str, body: str, tag: str, category: str) -> dict[str, Any]:
    global _next_id
    clean_tag = tag.strip() or "misc"
    clean_cat = category.strip() or "general"
    note = {
        "id": _next_id,
        "title": title.strip(),
        "body": body.strip(),
        "content": body.strip(),
        "tag": clean_tag,
        "tags": [clean_tag],
        "category": clean_cat,
        "created_at": datetime.now(),
    }
    _NOTES.append(note)
    _next_id += 1
    return deepcopy(note)


def update_note(
    note_id: int,
    *,
    title: str,
    body: str,
    tag: str,
    category: str,
) -> dict[str, Any] | None:
    for note in _NOTES:
        if note["id"] == note_id:
            clean_tag = tag.strip() or "misc"
            clean_cat = category.strip() or "general"
            note["title"] = title.strip()
            note["body"] = body.strip()
            note["content"] = body.strip()
            note["category"] = clean_cat
            note["tag"] = clean_tag
            note["tags"] = [clean_tag]
            return deepcopy(note)
    return None


def delete_note(note_id: int) -> bool:
    global _NOTES
    before = len(_NOTES)
    _NOTES = [n for n in _NOTES if n["id"] != note_id]
    return len(_NOTES) != before