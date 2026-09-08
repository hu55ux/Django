---
description: Django Forms, Templates, Views, Database, User/Superuser, and Admin Best Practices and Workflow Rules
---

# Django Full-Stack Best Practices Workflow

This workflow provides a standardized guide for implementing forms, templates, view handlers, database models, user management, and the admin interface in Django applications based on standard conventions.

## 1. Database & ORM Layer (`models.py`)

- **Model Definition**: Subclass `django.db.models.Model`.
- **Fields & Meta**:
  - Choose appropriate field types (`CharField`, `IntegerField`, `DateTimeField`, `ForeignKey`, etc.).
  - Always define `__str__(self)` for string representation.
  - Configure model metadata using `class Meta` (`ordering`, `verbose_name_plural`).
- **Migrations**: Always run `python manage.py makemigrations` and `python manage.py migrate` after model changes.
- **ORM Optimization**: Use `select_related()` for single-valued relationships (ForeignKey/OneToOne) and `prefetch_related()` for multi-valued relationships (ManyToMany/Reverse ForeignKey) to avoid N+1 queries.

---

## 2. User & Superuser Management (`django.contrib.auth`)

- **Authentication & Models**: Use Django's built-in `User` model or custom `AbstractUser`. Passwords must never be saved in plain text (`set_password()`).
- **Superuser Creation**: Create admin users via terminal: `python manage.py createsuperuser`.
- **Permissions & Access Control**:
  - Restrict view access using `@login_required` or `LoginRequiredMixin`.
  - Check privilege levels via `request.user.is_staff` and `request.user.is_superuser`.

---

## 3. Forms Layer (`forms.py`)

- **Form Class Definition**: Subclass `django.forms.Form` (or `forms.ModelForm`).
- **Field Configuration**:
  - Explicitly define field types (`CharField`, `IntegerField`, `EmailField`, `BooleanField`, etc.).
  - Set labels (`label="..."`), placeholders, widgets (`forms.TextInput`, `forms.NumberInput`, `forms.HiddenInput`), and CSS classes via `widget=forms.Widget(attrs={'class': '...', 'placeholder': '...'})`.
  - Provide user-friendly, localized error messages via `error_messages={'required': '...', 'invalid': '...'}`.
- **Field-Level Validation**:
  - Define `clean_<fieldname>(self)` for individual field checks.
  - Always clean/strip input strings (e.g., `.strip()`).
  - Raise `forms.ValidationError("...")` when validation fails.
- **Form-Level / Cross-Field Validation**:
  - Define `clean(self)` and execute `cleaned_data = super().clean()`.
  - Perform multi-field checks or validate against external domain context.
  - Raise `forms.ValidationError("...")` for form-level (non-field) errors.

---

## 4. Views Layer (`views.py`)

- **Handling GET Requests**:
  - For form display: Instantiate unbound form `form = TicketBookingForm(movie=movie)`.
  - For query filter forms: Instantiate bound form `filter_form = MovieFilterForm(request.GET or None)`.
- **Handling POST Requests**:
  - Instantiate bound form `form = TicketBookingForm(request.POST, movie=movie)`.
  - Check `if form.is_valid():`.
  - Extract validated inputs using `form.cleaned_data['field_name']`.
  - Delegate data mutations/bookings to data/model layer.
  - On backend/business logic errors, use `form.add_error(None, message)` and re-render template with the form instance.

---

## 5. Admin Panel (`admin.py`)

- **Model Registration**: Register models via `@admin.register(ModelName)` or `admin.site.register()`.
- **Customization**:
  - `list_display`: Customize list columns.
  - `list_filter`: Add filter sidebar.
  - `search_fields`: Enable search box (use `relation__field` for FKs).
  - `readonly_fields`, `ordering`, and `@admin.display`.

---

## 6. Templates Layer (`templates/`)

- **Form Tags & Security**:
  - Always include `{% csrf_token %}` inside `<form method="POST">`.
  - Use `novalidate` attribute on `<form>` tag if testing Django server-side validation explicitly.
- **Displaying Form Errors**:
  - Render non-field errors at the top (`form.non_field_errors`).
  - Render field labels, inputs, and field-specific errors (`form.field_name.errors`).

---

## 7. Verification & Testing

- Run system check:
  ```bash
  python manage.py check
  ```
- Run unit tests:
  ```bash
  python manage.py test
  ```
