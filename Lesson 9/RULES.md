# Django Forms, Templates və Views Qaydaları və Ən Yaxşı Təcrübələr (Best Practices)

Bu sənəd Django proqramlarında Formlar (`forms.py`), Şablonlar (`templates`) və Görüntülər (`views.py`) üçün müəyyən edilmiş əsas qaydaları və standartları ehtiva edir.

---

## 1. Django Forms (`forms.py`) Qaydaları

1. **Form Siniflərinin Təyin Edilməsi:**
   - Bütün formalar `django.forms.Form` (və ya `ModelForm`) sinfindən törədilməlidir.
   - Form sahələri uyğun tiplərlə təyin edilməlidir (`CharField`, `IntegerField`, `BooleanField`, `EmailField` və s.).

2. **Sahə Konfiqurasiyası və Widget-lər:**
   - Hər bir sahəyə aydın `label` və istifadəçiyə uyğun xəta mesajları (`error_messages`) verilməlidir.
   - CSS sinifləri və atributlar `widget=forms.WidgetType(attrs={'class': 'form-control', ...})` vasitəsilə təyin edilir.

3. **Sahə Səviyyəsində Doğrulama (`clean_<fieldname>`):**
   - Hər bir sahə üçün xüsusi doğrulama `clean_<fieldname>(self)` metodu ilə həyata keçirilir.
   - Mətni təmizləmək üçün `.strip()` istifadə edilir və şərt ödənmədikdə `raise forms.ValidationError("...")` çağırılır.

4. **Form Səviyyəsində / Çarpaz Doğrulama (`clean`):**
   - Birdən çox sahəni və ya domenin ümumi vəziyyətini (məsələn, mövcud bilet sayı) yoxlamaq üçün `clean(self)` metodu istifadə edilir.
   - İlk növbədə `cleaned_data = super().clean()` çağırılır və xəta olduqda `raise forms.ValidationError("...")` istifadə olunur.

---

## 2. Django Views (`views.py`) Qaydaları

1. **GET və POST Müraciətlərinin İdarə Edilməsi:**
   - `GET` müraciətində form obyektini bağlamadan və ya `request.GET` ilə yaradıb kontekstə ötürün.
   - `POST` müraciətində form obyektinə `request.POST` məlumatlarını ötürün: `form = TicketBookingForm(request.POST, movie=movie)`.

2. **Formun Yoxlanılması (`form.is_valid()`):**
   - Həmişə `if form.is_valid():` yoxlanışı aparılmalıdır.
   - Doğrulanmış məlumatlar yalnız `form.cleaned_data['sahə_adı']` vasitəsilə götürülməlidir.

3. **Xətaların İşlənməsi və Formun Yenidən Əks Olunması:**
   - Form keçərsiz olduqda və ya biznes mentiqində xəta baş verdikdə (`form.add_error(None, message)`), form obyekti eyni şablona ötürülərək istifadəçiyə xətalar göstərilməlidir.

---

## 3. Django Templates (`templates/`) Qaydaları

1. **Təhlükəsizlik və Form Teqləri:**
   - Hər bir `POST` formasının daxilində `{% csrf_token %}` yerləşdirilməlidir.

2. **Form Xətalarının Göstərilməsi:**
   - Form səviyyəsində olan xətalar üçün `{% if form.non_field_errors %}` bloku istifadə olunur.
   - Sahə səviyyəsində olan xətalar üçün `{% if form.field_name.errors %}` bloku istifadə olunur.

3. **Form Sahələrinin Render Olunması:**
   - Sahələrin etiketləri `{{ form.field_name.label_tag }}` və giriş elementləri `{{ form.field_name }}` vasitəsilə göstərilməlidir.

---

## 4. Test və Yoxlama Qaydaları

- Dəyişikliklərdən sonra sistem yoxlaması:
  ```bash
  python manage.py check
  ```
- Unit testlərin icrası:
  ```bash
  python manage.py test
  ```
