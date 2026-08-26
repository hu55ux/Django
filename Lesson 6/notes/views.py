from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.utils.html import escape
from django.urls import reverse
from django.http import HttpResponse, HttpRequest

from . import data


def html_shell(title: str, body: str) -> str:
    safe_title = escape(title)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: #f4f7fb;
            color: #1f2937;
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 24px 40px;
        }}

        .nav {{
            background: #ffffff;
            border-bottom: 1px solid #e5e7eb;
            padding: 16px 24px;
            margin-bottom: 32px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }}

        .nav-inner {{
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            gap: 12px;
        }}

        .nav a {{
            text-decoration: none;
            color: #374151;
            font-weight: 600;
            padding: 8px 14px;
            border-radius: 8px;
            transition: 0.2s;
        }}

        .nav a:hover {{
            background: #eaf2ff;
            color: #0b57d0;
        }}

        h1 {{
            color: #111827;
            margin-bottom: 20px;
        }}

        p {{
            margin: 10px 0;
        }}

        a {{
            color: #0b57d0;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        .muted {{
            color: #6b7280;
            font-size: 0.95rem;
        }}

        code {{
            background: #eef2f7;
            color: #374151;
            padding: 3px 7px;
            border-radius: 5px;
            font-family: Consolas, monospace;
        }}

        ul.notes {{
            list-style: none;
            padding: 0;
            margin-top: 20px;
        }}

        ul.notes li {{
            background: #ffffff;
            padding: 16px 18px;
            margin-bottom: 12px;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
            transition: transform 0.15s, box-shadow 0.15s;
        }}

        ul.notes li:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 14px rgba(0, 0, 0, 0.08);
        }}

        ul.notes li > a {{
            font-size: 1.05rem;
            font-weight: bold;
            margin-right: 8px;
        }}

        form {{
            background: #ffffff;
            padding: 28px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            max-width: 650px;
        }}

        form label {{
            display: block;
            font-weight: 600;
            margin-top: 16px;
            margin-bottom: 6px;
        }}

        form input[type="text"],
        form input:not([type]),
        form textarea {{
            display: block;
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #d1d5db;
            border-radius: 7px;
            font-size: 1rem;
            font-family: inherit;
            outline: none;
            transition: border 0.2s, box-shadow 0.2s;
        }}

        form input:focus,
        form textarea:focus {{
            border-color: #0b57d0;
            box-shadow: 0 0 0 3px rgba(11, 87, 208, 0.12);
        }}

        textarea {{
            resize: vertical;
        }}

        button {{
            background: #0b57d0;
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 7px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }}

        button:hover {{
            background: #0847ad;
        }}

        button:active {{
            transform: scale(0.98);
        }}

        .btn-danger {{
            background: #dc2626;
            color: white;
        }}

        .btn-danger:hover {{
            background: #b91c1c;
        }}

        .btn-secondary {{
            background: #f3f4f6;
            color: #374151;
            text-decoration: none;
            display: inline-block;
            padding: 10px 18px;
            border-radius: 7px;
            font-weight: 600;
            border: 1px solid #d1d5db;
            transition: background 0.2s;
        }}

        .btn-secondary:hover {{
            background: #e5e7eb;
            color: #111827;
            text-decoration: none;
        }}

        .delete-card {{
            background: #ffffff;
            padding: 32px;
            border-radius: 12px;
            border: 1px solid #fee2e2;
            box-shadow: 0 4px 16px rgba(220, 38, 38, 0.08);
            max-width: 550px;
        }}

        .delete-card h1 {{
            color: #dc2626;
            font-size: 1.5rem;
            margin-top: 0;
        }}

        .note-preview {{
            background: #fcfcfd;
            border-left: 4px solid #dc2626;
            padding: 12px 16px;
            margin: 16px 0 24px;
            border-radius: 0 8px 8px 0;
        }}

        .actions {{
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }}

        .actions a {{
            display: inline-block;
            padding: 8px 14px;
            background: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 7px;
            text-decoration: none;
        }}

        .actions a:hover {{
            background: #f3f4f6;
            text-decoration: none;
        }}

        @media (max-width: 600px) {{
            .container {{
                padding-left: 15px;
                padding-right: 15px;
            }}

            .nav-inner {{
                flex-wrap: wrap;
            }}

            form {{
                padding: 20px;
            }}
        }}
    </style>
</head>

<body>

    <nav class="nav">
        <div class="nav-inner">
            <a href="{escape(reverse('home'))}">Home</a>
            <a href="{escape(reverse('about'))}">About</a>
            <a href="{escape(reverse('notes_list'))}">Notes</a>
        </div>
    </nav>

    <main class="container">
        {body}
    </main>

</body>
</html>
"""


def _csrf_field(request: HttpRequest) -> str:
    token = get_token(request)
    return f"<input type='hidden' name='csrfmiddlewaretoken' value='{escape(token)}'>"


def home(request: HttpRequest) -> HttpResponse:
    body = f"""
    <h1>Knowledge Hub</h1>
    <p>Welcome to Knowledge Hub!</p>
    <p class='muted'>
        <a href="{escape(reverse('notes_list'))}">Go to Notes list</a>
    </p>
    """
    return HttpResponse(html_shell("Knowledge Hub - Home", body))


def about(request: HttpRequest) -> HttpResponse:
    body = """
        <h1>About Knowledge Hub Project</h1>

        <p>
            Knowledge Hub is a simple Django web application designed
            to store and organize useful notes and learning materials.
        </p>

        <p>
            Users can browse notes, view detailed information,
            and explore content by tags and categories.
        </p>

        <p class='muted'>
            This project was created to practice Django views,
            URL routing, HTTP requests and responses.
        </p>
    """
    return HttpResponse(html_shell("About Knowledge Hub", body))


def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get("tag")
    raw_category = request.GET.get("category")

    all_notes = data.list_notes()
    notes = all_notes

    if raw_tag and raw_tag.strip():
        tag_filter = raw_tag.strip().lower()
        notes = [n for n in notes if n["tag"].lower() == tag_filter]

    if raw_category and raw_category.strip():
        category_filter = raw_category.strip().lower()
        notes = [n for n in notes if n["category"].lower() == category_filter]

    items: list[str] = []

    for note in notes:
        url = reverse("note_detail", kwargs={"note_id": note["id"]})

        items.append(
            f"""
            <li>
                <a href="{escape(url)}">
                    {escape(note["title"])}
                </a>

                <span class="muted">
                    (tag: {escape(note["tag"])}, category: {escape(note["category"])})
                </span>
            </li>
            """
        )

    reset_url = escape(reverse("notes_list"))
    create_url = escape(reverse("note_create"))

    all_tags = sorted(list(set(n["tag"] for n in all_notes)))
    all_categories = sorted(list(set(n["category"] for n in all_notes)))

    tag_options = ['<option value="">-- All Tags --</option>']
    for t in all_tags:
        selected = "selected" if raw_tag and raw_tag.strip().lower() == t.lower() else ""
        tag_options.append(f'<option value="{escape(t)}" {selected}>{escape(t.capitalize())}</option>')

    category_options = ['<option value="">-- All Categories --</option>']
    for c in all_categories:
        selected = "selected" if raw_category and raw_category.strip().lower() == c.lower() else ""
        category_options.append(f'<option value="{escape(c)}" {selected}>{escape(c.capitalize())}</option>')

    filters = f"""
        <form method="GET" action="{reset_url}">

            <h3 style="margin-top: 0; margin-bottom: 12px;">Filter Notes</h3>

            <div style="display: flex; gap: 16px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 180px;">
                    <label style="margin-top: 0;">Tag</label>
                    <select name="tag">
                        {"".join(tag_options)}
                    </select>
                </div>

                <div style="flex: 1; min-width: 180px;">
                    <label style="margin-top: 0;">Category</label>
                    <select name="category">
                        {"".join(category_options)}
                    </select>
                </div>
            </div>

            <p style="margin-top: 16px;">
                <button type="submit">Apply Filter</button>
                <a href="{reset_url}" class="btn-secondary" style="margin-left: 8px; font-size: 0.9rem; padding: 9px 16px;">Reset</a>
            </p>

        </form>
    """

    body = f"""
        <h1>Notes</h1>

        {filters}

        <p style="margin-top: 24px;">
            <a href="{create_url}" style="display: inline-block; background: #0b57d0; color: white; padding: 10px 18px; border-radius: 8px; font-weight: 600; text-decoration: none;">
                + Create Note
            </a>
        </p>

        <ul class="notes">
            {"".join(items) if items else "<li>Notes not found</li>"}
        </ul>
    """

    return HttpResponse(html_shell("Notes — List", body))


def note_detail(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse(
            html_shell(
                "404 — Not Found",
                f"""
                <h1>Note Not Found</h1>
                <p class="muted">id = {escape(str(note_id))}</p>
                <p><a href="{escape(reverse("notes_list"))}">Return to notes list</a></p>
                """,
            ),
            status=404,
        )

    edit_url = escape(reverse("note_edit", kwargs={"note_id": note_id}))
    delete_url = escape(reverse("note_delete", kwargs={"note_id": note_id}))
    list_url = escape(reverse("notes_list"))

    body = f"""
        <h1>{escape(note['title'])}</h1>
        <p class="muted">ID: {note["id"]} | Tag: {escape(note["tag"])} | Category: {escape(note["category"])}</p>
        <p style="font-size: 1.1rem; line-height: 1.7; margin: 20px 0;">{escape(note['body'])}</p>

        <div style="display: flex; gap: 12px; margin-top: 24px;">
            <a href="{edit_url}" style="background: #0b57d0; color: white; padding: 8px 16px; border-radius: 6px; font-weight: 600; text-decoration: none;">Edit Note</a>
            <a href="{delete_url}" style="background: #dc2626; color: white; padding: 8px 16px; border-radius: 6px; font-weight: 600; text-decoration: none;">Delete Note</a>
            <a href="{list_url}" class="btn-secondary">Back to List</a>
        </div>
    """
    return HttpResponse(html_shell(note["title"], body))


def note_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        if not title.strip():
            err = "<p style='color:#dc2626; font-weight:600; margin-bottom:12px;'>Title cannot be empty!</p>"
        else:
            created = data.create_note(
                title=title,
                body=note_body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("note_detail", note_id=created["id"])
    else:
        err = ""

    action = escape(reverse("note_create"))
    list_url = escape(reverse("notes_list"))

    form = f"""
    <h1>Create New Note</h1>
    {err}
    <form method="POST" action="{action}">
        {_csrf_field(request)}
        <p>
            <label>Title *</label>
            <input type="text" name="title" placeholder="Enter note title..." required>
        </p>
        <p>
            <label>Text</label>
            <textarea name="body" rows="5" placeholder="Enter note content..."></textarea>
        </p>
        <p>
            <label>Tag</label>
            <input type="text" name="tag" placeholder="e.g. python, django">
        </p>
        <p>
            <label>Category</label>
            <input type="text" name="category" placeholder="e.g. backend, frontend">
        </p>
        <div style="margin-top: 24px; display: flex; gap: 12px; align-items: center;">
            <button type="submit">Create Note</button>
            <a href="{list_url}" class="btn-secondary">Cancel</a>
        </div>
    </form>
    """
    return HttpResponse(html_shell("Create Note", form))


def note_edit(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse(
            html_shell(
                "404 — Not Found",
                f"""
                <h1>Cannot Edit</h1>
                <p class="muted">Note with id={escape(str(note_id))} does not exist.</p>
                <p><a href="{escape(reverse("notes_list"))}">Back to list</a></p>
                """,
            ),
            status=404,
        )

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        if not title.strip():
            err = '<p style="color:#dc2626; font-weight:600; margin-bottom:12px;">Title cannot be empty!</p>'
            note = {
                **note,
                "title": title,
                "body": note_body,
                "tag": tag,
                "category": category,
            }
        else:
            data.update_note(
                note_id,
                title=title,
                body=note_body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("note_detail", note_id=note_id)
    else:
        err = ""

    title_e = escape(note["title"])
    body_e = escape(note["body"])
    tag_e = escape(note["tag"])
    category_e = escape(note["category"])
    action_url = escape(reverse("note_edit", kwargs={"note_id": note_id}))
    detail_url = escape(reverse("note_detail", kwargs={"note_id": note_id}))

    form = f"""
    <h1>Edit Note</h1>
    {err}
    <form method="POST" action="{action_url}">
        {_csrf_field(request)}
        <p>
            <label>Title *</label>
            <input type="text" name="title" value="{title_e}" required>
        </p>
        <p>
            <label>Text</label>
            <textarea name="body" rows="6">{body_e}</textarea>
        </p>
        <p>
            <label>Tag</label>
            <input type="text" name="tag" value="{tag_e}">
        </p>
        <p>
            <label>Category</label>
            <input type="text" name="category" value="{category_e}">
        </p>
        <div style="margin-top: 24px; display: flex; gap: 12px; align-items: center;">
            <button type="submit">Save Changes</button>
            <a href="{detail_url}" class="btn-secondary">Cancel</a>
        </div>
    </form>
    """
    return HttpResponse(html_shell("Edit Note", form))


def note_delete(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse(
            html_shell(
                "404 — Not Found",
                f"""
                <h1>Cannot Delete</h1>
                <p class="muted">Note with id={escape(str(note_id))} does not exist.</p>
                <p><a href="{escape(reverse("notes_list"))}">Back to list</a></p>
                """,
            ),
            status=404,
        )

    if request.method == "POST":
        data.delete_note(note_id)
        return redirect("notes_list")

    detail_url = escape(reverse("note_detail", kwargs={"note_id": note_id}))
    action_url = escape(reverse("note_delete", kwargs={"note_id": note_id}))

    body = f"""
    <div class="delete-card">
        <h1>Confirm Deletion</h1>
        <p>Are you sure you want to permanently delete this note?</p>
        
        <div class="note-preview">
            <strong>{escape(note["title"])}</strong>
            <p class="muted" style="margin: 4px 0 0 0;">Tag: {escape(note["tag"])} | Category: {escape(note["category"])}</p>
        </div>

        <form method="POST" action="{action_url}" style="padding:0; border:none; box-shadow:none; background:transparent;">
            {_csrf_field(request)}
            <div style="display: flex; gap: 12px; align-items: center;">
                <button type="submit" class="btn-danger">Yes, Delete Note</button>
                <a href="{detail_url}" class="btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
    """
    return HttpResponse(html_shell("Delete Note", body))