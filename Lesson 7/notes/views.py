from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from . import data


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "page_title": "Knowledge Hub",
        "welcome_text": "Welcome to Knowledge Hub!",
    }
    return render(request, "notes/home.html", context)


def about(request: HttpRequest) -> HttpResponse:
    context = {
        "project_name": "Knowledge Hub",
        "author": "Nadir Zamanov",
    }
    return render(request, "notes/about.html", context)


def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get("tag")
    raw_category = request.GET.get("category")

    all_notes = data.list_notes()
    filtered_notes = all_notes

    if raw_tag and raw_tag.strip():
        tag_filter = raw_tag.strip().lower()
        filtered_notes = [n for n in filtered_notes if n["tag"].lower() == tag_filter]

    if raw_category and raw_category.strip():
        cat_filter = raw_category.strip().lower()
        filtered_notes = [n for n in filtered_notes if n["category"].lower() == cat_filter]

    all_tags = sorted(list(set(n["tag"] for n in all_notes)))
    all_categories = sorted(list(set(n["category"] for n in all_notes)))

    context = {
        "notes": filtered_notes,
        "all_tags": all_tags,
        "all_categories": all_categories,
        "selected_tag": raw_tag.strip() if raw_tag else "",
        "selected_category": raw_category.strip() if raw_category else "",
    }
    return render(request, "notes/notes_list.html", context)


def note_detail(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return render(request, "notes/note_detail.html", {"note": None}, status=404)
    return render(request, "notes/note_detail.html", {"note": note})


def note_create(request: HttpRequest) -> HttpResponse:
    err = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        if not title.strip():
            err = "Title cannot be empty!"
        else:
            created = data.create_note(
                title=title,
                body=body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("note_detail", note_id=created["id"])

    return render(request, "notes/note_create.html", {"err": err})


def note_edit(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return render(request, "notes/note_detail.html", {"note": None}, status=404)

    err = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        if not title.strip():
            err = "Title cannot be empty!"
            note = {
                **note,
                "title": title,
                "body": body,
                "tag": tag,
                "category": category,
            }
        else:
            data.update_note(
                note_id,
                title=title,
                body=body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("note_detail", note_id=note_id)

    return render(request, "notes/note_edit.html", {"note": note, "err": err})


def note_delete(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return render(request, "notes/note_detail.html", {"note": None}, status=404)

    if request.method == "POST":
        data.delete_note(note_id)
        return redirect("notes_list")

    return render(request, "notes/note_delete.html", {"note": note})