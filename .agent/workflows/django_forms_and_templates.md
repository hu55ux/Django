---
description: Django Forms, Templates, and Views Best Practices and Workflow Rules
---

# Django Forms, Templates & Views Best Practices Workflow

This workflow provides a standardized guide for implementing forms, templates, view handlers, and validation in Django applications based on the latest conventions.

## 1. Forms Layer (`forms.py`)

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
  - Perform multi-field checks or validate against external domain context (e.g., checking available seats or matching passwords).
  - Raise `forms.ValidationError("...")` for form-level (non-field) errors.

---

## 2. Views Layer (`views.py`)

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

## 3. Templates Layer (`templates/`)

- **Form Tags & Security**:
  - Always include `{% csrf_token %}` inside `<form method="POST">`.
  - Use `novalidate` attribute on `<form>` tag if testing Django server-side validation explicitly.
- **Displaying Form Errors**:
  - Render non-field errors at the top:
    ```html
    {% if form.non_field_errors %}
        <div class="alert alert-error">
            {% for error in form.non_field_errors %}
                <div>⚠️ {{ error }}</div>
            {% endfor %}
        </div>
    {% endif %}
    ```
  - Render field labels, inputs, and field-specific errors:
    ```html
    <div class="form-group">
        {{ form.field_name.label_tag }}
        {{ form.field_name }}
        {% if form.field_name.errors %}
            <div class="field-error">
                {% for error in form.field_name.errors %}
                    <div>⚠️ {{ error }}</div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
    ```

---

## 4. Verification & Testing

- Run system check:
  ```bash
  python manage.py check
  ```
- Run unit tests:
  ```bash
  python manage.py test
  ```
