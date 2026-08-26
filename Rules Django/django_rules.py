"""
===============================================================================
                     DJANGO FRAMEWORK - ƏSAS QAYDALAR VƏ ANLAYIŞLAR
===============================================================================
Bu fayl Django Veb Freymvorkunun ümumi mahiyyətini, arxitekturasını (MVT), 
əsas əmrlərini, standart layihə strukturunu və Django Admin Panelinin 
qurulması, özəlləşdirilməsi qaydalarını aydın, səliqəli dildə izah edir.
===============================================================================
"""

# =============================================================================
# 1. DJANGO NƏDİR? (WHAT IS DJANGO?)
# =============================================================================

"""
1.1. UMUMİ TƏRİF
----------------
Django — Python dilində yazılmış, yüksək səviyyəli (high-level), açıq mənbəli 
veb freymvorkdur (Web Framework).

1.2. DJANGO-NUN ƏSAS MƏQSƏDİ VƏ FƏLSƏFƏSİ
------------------------------------------
- "Batteries Included" (Hər şey daxildir): Django daxilində veb tətbiq yaratmaq 
  üçün lazım olan demək olar ki, bütün alətləri (Autentifikasiya, Admin Panel, 
  ORM Verilənlər Bazası, Forma idarəetməsi, Təhlükəsizlik) hazır təqdim edir.
- "Don't Repeat Yourself" (DRY): Kod təkrarının qarşısını almağı və təkrar 
  istifadə edilə bilən komponentlər yaratmağı həvəsləndirir.
- Sürətli İnkişaf (Rapid Development) və Yüksək Təhlükəsizlik: SQL Injection, 
  XSS, CSRF kimi təhlükəsizlik xətalarından avtomatik qoruyur.
"""


# =============================================================================
# 2. DJANGO ARXİTEKTURASI: MVT (MODEL - VIEW - TEMPLATE)
# =============================================================================

"""
Django klassik MVC (Model-View-Controller) şablonunun özünəməxsus variantı olan 
MVT (Model-View-Template) arxitekturasından istifadə edir:

-------------------------------------------------------------------------------
| Komponent | Təsviri və Vəzifəsi                                             |
-------------------------------------------------------------------------------
| MODEL     | Verilənlər bazası (Database) strukturu və məlumat modelləri.    |
|           | Python klassları vasitəsilə cədvəlləri təyin edir (ORM).        |
-------------------------------------------------------------------------------
| VIEW      | Biznes məntiqi (Business Logic). Sorğunu (HttpRequest) qəbul    |
|           | edir, modeldən məlumat alır və cavabı (HttpResponse) qaytarır.  |
-------------------------------------------------------------------------------
| TEMPLATE  | İstifadəçiyə görünən interfeys (HTML/UI). Məlumatların         |
|           | dinamik olaraq HTML daxilində nümayiş etdirilməsini təmin edir. |
-------------------------------------------------------------------------------

Sorğunun İşləmə Sırası (Request Lifecycle):
User Browser -> URL Pattern -> View -> (Model / Database) -> Template -> Response
"""


# =============================================================================
# 3. ƏSAS ƏMRLƏR (ESSENTIAL CLI COMMANDS)
# =============================================================================

"""
1. Yeni Django Layihəsi Yaratmaq:
   $ django-admin startproject project_name .

2. Yeni Tətbiq (App) Yaratmaq:
   $ python manage.py startapp app_name

3. Lokal İcra Serverini Başlatmaq:
   $ python manage.py runserver

4. Verilənlər Bazası Miqrasiya Faylları Yaratmaq:
   $ python manage.py makemigrations

5. Miqrasiyaları Bazaya Tətbiq Etmək:
   $ python manage.py migrate

6. Superuser (Admin İstifadəçisi) Yaratmaq:
   $ python manage.py createsuperuser
"""


# =============================================================================
# 4. LAYİHƏ VƏ TƏTBİQ STRUKTURU (PROJECT & APP STRUCTURE)
# =============================================================================

"""
Standard Layihə Qovluqları:

📁 project_root/
├── 📄 manage.py            # Layihə əmrlərini icra etmək üçün skript
├── 📁 config/              # Əsas konfiqurasiya papkası
│   ├── 📄 __init__.py
│   ├── 📄 settings.py     # Layihənin bütün parametrləri (DB, Apps, Middleware)
│   ├── 📄 urls.py         # Əsas URL marşrutlaşdırması (Routing)
│   ├── 📄 wsgi.py         # WSGI web server inteqrasiyası
│   └── 📄 asgi.py         # Asinxron (Async) server inteqrasiyası
└── 📁 my_app/              # Yaratdığımız tətbiq (App)
    ├── 📄 admin.py         # Admin panel qeydiyyatları
    ├── 📄 apps.py          # Tətbiqin konfiqurasiyası
    ├── 📄 models.py        # Database modelləri
    ├── 📄 views.py         # Biznes məntiqi / Funksiyalar
    ├── 📄 urls.py          # Tətbiqə özəl URL marşrutları
    └── 📁 migrations/      # Bazanın dəyişiklik tarixçəsi
"""


# =============================================================================
# 5. DJANGO ADMİN PANELİ VƏ ÖZƏLLƏŞDİRİLMƏSİ (DJANGO ADMIN PANEL)
# =============================================================================

"""
5.1. ADMİN PANELİ NƏDİR?
------------------------
Django Admin Paneli — Avtomatik generasiya olunan, verilənlər bazası 
yazılarını (CRUD əməliyyatları: Create, Read, Update, Delete) idarə etmək 
üçün nəzərdə tutulmuş hazır inzibatçı idarəetmə panelidir.

5.2. ADMİN PANELİNƏ GİRİŞ VƏ SUPERUSER YARADILMASI
--------------------------------------------------
1. Miqrasiyaların icra olunduğundan əmin olun: `python manage.py migrate`
2. İnzibatçı istifadəçisi (Superuser) yaradın:
   $ python manage.py createsuperuser
   (İstifadəçi adı, e-poçt və parol daxil edilir)
3. Server işə salındıqda keçid ünvanı: `http://127.0.0.1:8000/admin/`

5.3. MODELLƏRİN ADMİN PANELƏ QEYDİYYATI (`admin.py`)
----------------------------------------------------
Yaratdığımız verilənlər bazası modelini admin paneldə göstərmək üçün tətbiqin 
`admin.py` faylında qeydiyyatdan keçirməliyik.

Nümunə (`my_app/admin.py`):
"""

# Metod 1: Sadə Qeydiyyat
# from django.contrib import admin
# from .models import Product
# admin.site.register(Product)

# Metod 2: ModelAdmin Sinfi ilə Özəlləşdirilmiş Qeydiyyat (Tövsiyə olunan)
"""
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Siyahı görünüşündə hansı sütunlar çıxsın:
    list_display = ('id', 'name', 'price', 'is_active', 'created_at')
    
    # Hansı sütunlara vuraraq detallı səhifəyə keçmək olar:
    list_display_links = ('id', 'name')
    
    # Sağ tərəfdə filtrləmə paneli yaradır:
    list_filter = ('is_active', 'created_at')
    
    # Axtarış paneli yaradır (göstərilən sahələrdə axtarır):
    search_fields = ('name', 'description')
    
    # Birbaşa siyahıda dəyişdirilə bilən sahələr:
    list_editable = ('price', 'is_active')
    
    # Neçə element bir səhifədə göstərilsin (Pagination):
    list_per_page = 20
"""


# =============================================================================
# 6. CRUD ƏMƏLİYYATLARI VƏ VIEW MƏNTİQİ (KNOWLEDGE HUB PRAKTİKASI)
# =============================================================================

"""
6.1. CRUD NƏDİR?
----------------
CRUD — Veb tətbiqlərdə verilənlər üzərində aparılan 4 əsas əməliyyatdır:
- C (Create)  : Yeni obyekt yaradılması (`note_create` funksiyası).
- R (Read)    : Obyektlərin siyahısı və detal baxışı (`notes_list`, `note_detail`).
- U (Update)  : Mövcud obyektin redaktə olunması (`note_edit` funksiyası).
- D (Delete)  : Obyektin sistemdən silinməsi (`note_delete` funksiyası).

6.2. KRİTİK DJANGO FUNKSİYALARI VƏ ANLAYIŞLARI (KNOWLEDGE HUB İZAHI)
---------------------------------------------------------------------

1. `CSRF Qorunması (Cross-Site Request Forgery - Dərin İzah)`:
   a) **CSRF Hücumu Nədir?**
      - Zərərli 3-cü tərəf saytı, istifadəçinin brauzerində aktiv olan sessiyadan 
        (session cookies) istifadə edərək, istifadəçinin xəbəri olmadan bizim sayta 
        icazəsiz dəyişiklik edən POST/PUT/DELETE sorğuları göndərir.

   b) **Django Necə Qoruyur? (CSRF Middleware)**
      - Django daxili `CsrfViewMiddleware` vasitəsilə hər bir state-changing (POST, PUT, 
        PATCH, DELETE) sorğuda gizli bir token göndərilməsini tələb edir.
      - Django brauzerə `csrftoken` adında xüsusi cookie yerləşdirir və forma daxilindəki 
        `csrfmiddlewaretoken` dəyərini həmin cookie ilə müqayisə edir. Tokenlər üst-üstə 
        düşmədikdə `403 Forbidden` xətası qaytarır.

   c) **Token-in Formaya Daxil Edilməsi Üsulları:**
      - **HTML Template ilə:** Forms daxilində `{% csrf_token %}` teqini yazmaqla.
      - **Pure Python / View-da (Knowledge Hub):** `django.middleware.csrf.get_token(request)` 
        funksiyasını çağıraraq gizli input kimi əlavə etmək:
        `<input type='hidden' name='csrfmiddlewaretoken' value='{get_token(request)}' />`

   d) **İstisnalar və Dekaratorlar:**
      - `@csrf_exempt`: Çox xüsusi hallarda (məsələn, xarici webhook-lar üçün) CSRF 
        yoxlamasını müvəqqəti söndürür (ehtiyatlı istifadə edilməlidir!).
      - `@csrf_protect`: View üçün CSRF yoxlamasını məcburi aktiv edir.

   e) **AJAX / Single Page Apps (SPA):**
      - JavaScript (Fetch/Axios) vasitəsilə POST sorğusu göndərdikdə `X-CSRFToken` HTTP 
        header-i daxilində cookie-dəki `csrftoken` göndərilməlidir.

2. `redirect("route_name", **kwargs)`:
   - Forma göndərildikdən (POST) sonra istifadəçini başqa səhifəyə yönləndirir.
   - Səhifənin yenilənməsi zamanı təkrarlanan POST sorğusunun (PRG Pattern) qarşısını alır.

3. `reverse("route_name", kwargs={"id": 1})`:
   - URL-in adından (`name="note_detail"`) istifadə edərək marşrut ünvanını (`/notes/1/`) 
     dinamik olaraq generasiya edir. Kodda hardcode URL yazılışının qarşısını alır.

4. `request.GET.get("param")` & Dinamik Filtrləmə:
   - URL query parametrlərini (`/notes/?tag=python&category=backend`) oxuyur.
   - Unikal tag və kateqoriya siyahısını toplayaraq HTML `<select>` dropdown menyuları 
     vasitəsilə dinamik süzgəcləmə və sıfırlama (Reset) imkanı yaradır.

5. `404 Not Found İdarəetməsi`:
   - Müraciət edilən id üzrə obyekt tapılmadıqda status=404 kodu ilə istifadəçiyə 
     səliqəli xəta mesajı qaytarılır.

6. `escape()` (`from django.utils.html import escape`):
   - **XSS (Cross-Site Scripting)** təhlükəsizlik hücumlarının qarşısını alır.
   - İstifadəçinin daxil etdiyi xüsusi HTML/JS simvollarını (`<`, `>`, `&`, `"`, `'`) 
     təhlükəsiz HTML entity-lərinə (`&lt;`, `&gt;`) çevirir. Zərərli script-lərin icrasını 
     və sayt dizaynının pozulmasını əngəlləyir.

7. `html_shell(title, body)` Layout Funksiyası:
   - **DRY (Don't Repeat Yourself)** prinsipini təmin edir.
   - Hər bir view-da `<!DOCTYPE html>`, `<head>`, `<style>`, `<nav>` kimi ümumi HTML 
     skeletini dəfələrlə təkrar yazmaq yerinə, bütün view-ları vahid dizayn çərçivəsində 
     birləşdirən köməkçi wrapper funksiyadır.

6.3. KNOWLEDGE HUB-DA VIEW STRUCTURE NÜMUNƏSİ:
----------------------------------------------
```python
# UPDATE (Edit) View Nümunəsi:
def note_edit(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse("404 Not Found", status=404)

    if request.method == "POST":
        title = request.POST.get("title", "")
        # Məlumatları yeniləyirik:
        data.update_note(note_id, title=title, ...)
        return redirect("note_detail", note_id=note_id)
    
    # GET: Doldurulmuş forma qaytarılır
    return HttpResponse(render_edit_form(note))

# DELETE View Nümunəsi:
def note_delete(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse("404 Not Found", status=404)

    if request.method == "POST":
        data.delete_note(note_id)
        return redirect("notes_list")
    
    # GET: Təsdiqləmə kartı nümayiş olunur
    return HttpResponse(render_delete_confirmation(note))
```
"""


# =============================================================================
# 7. DJANGO TEMPLATES ARXİTEKTURASI VƏ İRSİLİK (LESSON 7 PRAKTİKASI)
# =============================================================================

"""
7.1. TEMPLATES NƏDİR VƏ STRUKTURU
----------------------------------
Django Templates — Python məntiqi ilə HTML interfeysini ayıran dinamik şablonlaşdırma sistemidir.
Fayllar adətən layihənin kök qovluğundakı `templates/` papkasında saxlanılır.

`settings.py` Konfiqurasiyası:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    }
]

7.2. ƏSAS TEMPLATE TEQLƏRİ (TAGS) VƏ İRSİLİK (INHERITANCE)
----------------------------------------------------------
1. `{% extends "base.html" %}`:
   - Ana HTML şablonundan irsilik alır. Şablon faylının ƏN ÜST xəttində yazılmalıdır.

2. `{% block content %} ... {% endblock %}`:
   - Ana şablonda (`base.html`) yer ayrılır, alt şablonlar həmin hissəni öz məzmunu ilə doldurur.

3. `{% include "notes/_page_header.html" %}`:
   - Təkrar istifadə olunan komponenti (məsələn, Navbar, Header, Footer) şablona daxil edir.

4. `{% url 'route_name' arg1 %}`:
   - URL-i dinamik çağırır (`<a href="{% url 'note_detail' note.id %}">`).

5. `{% csrf_token %}`:
   - Formanın daxilində POST təhlükəsizlik tokeni yerləşdirir.

6. `{% for ... in ... %}` & `{% empty %}`:
   - Siyahı boş olduqda `{% empty %}` bloku avtomatik işə düşür.

7. `{% with total=notes|length %}`:
   - Şablon daxilində müvəqqəti dəyişən yaradır.

7.3. ƏSAS TEMPLATE FİLTRLƏRİ (FILTERS)
---------------------------------------
- `{{ note.title|title }}` : İlk hərfləri böyük edir.
- `{{ note.category|upper }}` : Mətni tam böyük hərfə çevirir.
- `{{ note.category|capfirst }}` : Yalnız ilk hərfi böyük edir.
- `{{ notes|length }}` : Siyahının uzunluğunu qaytarır.
- `{{ note.created_at|date:"j F Y" }}` : Tarixi formatlayır (məs: 24 August 2026).
- `{{ note.body|truncatechars:100 }}` : Mətni verilən simvol sayına qədər kəsir.

7.4. VIEW-DA `render()` İSTİFADƏSİ VƏ ARGUMENTLƏRİ
---------------------------------------------------
`render(request, template_name, context=None, content_type=None, status=None, using=None)`

Parametrlər:
- `request`: Müraciət edən client-in `HttpRequest` obyekti (məcburi).
- `template_name`: Şablonun nisbi yolu (`"notes/notes_list.html"`) (məcburi).
- `context`: Şablona ötürülən məlumat lüğəti (dict) (məs: `{"notes": notes}`).
- `status`: HTTP status kodu (məs: `200` OK, `404` Not Found, `403` Forbidden).
- `content_type`: MIME cavab növü (susmaya görə `"text/html"`).
- `using`: İstifadə olunacaq şablon mühərriki (Engine).

7.5. `HttpRequest` OBYEKTİNİN BÜTÜN ƏSAS ATRİBUTLARI VƏ İMKANLARI
------------------------------------------------------------------
View funksiyasına birinci parametr kimi gələn `request: HttpRequest` obyektindən oxuya bildiyimiz məlumatlar:

1. `request.method`:
   - Sorğunun HTTP metodunu str olaraq qaytarır (`"GET"`, `"POST"`, `"PUT"`, `"DELETE"`).

2. `request.GET`:
   - URL-dəki query parametrlərini ehtiva edən QueryDict obyektidir (məs: `/notes/?tag=python` -> `request.GET.get("tag")`).

3. `request.POST`:
   - HTML forması vasitəsilə POST sorğusunda daxil edilən sahələri ehtiva edən QueryDict (məs: `request.POST.get("title")`).

4. `request.FILES`:
   - `multipart/form-data` formalardan yüklənən faylları ehtiva edən dictionary (məs: `request.FILES['avatar']`).

5. `request.COOKIES`:
   - İstifadəçinin brauzerindən gələn bütün Cookie-ləri ehtiva edən lüğət (məs: `request.COOKIES.get('csrftoken')`).

6. `request.META`:
   - Server və HTTP header məlumatlarını ehtiva edir (məs: `request.META.get('HTTP_USER_AGENT')`, `request.META.get('REMOTE_ADDR')`).

7. `request.headers`:
   - Case-insensitive (böyük-kiçik hərf fərqi olmayan) HTTP Header-lərə rahat çıxış verir (məs: `request.headers.get('User-Agent')`).

8. `request.body`:
   - HTTP sorğusunun xam (raw) byte məzmunu. REST API və ya JSON sorğularında `json.loads(request.body)` kimi istifadə edilir.

9. `request.path` & `request.path_info`:
   - Müraciət edilən tam URL yolunu (domain və query olmadan) qaytarır (məs: `/notes/create/`).

10. `request.get_full_path()`:
    - URL path və query parametrlərini birlikdə qaytarır (məs: `/notes/?tag=python&category=backend`).

11. `request.build_absolute_uri()`:
    - Domen adı daxil olmaqla tam Absolyut URL-i qaytarır (məs: `http://127.0.0.1:8000/notes/1/`).

12. `request.user`:
    - Aktiv avtentifikasiya olunmuş istifadəçi obyekti (`django.contrib.auth` aktiv olduqda).

13. `request.session`:
    - İstifadəçinin serverdəki sessiya məlumatları (dict kimi işlədilir: `request.session['theme'] = 'dark'`).
"""


# =============================================================================
# 8. QISA XÜLASƏ ÇAPI
# =============================================================================

def show_django_summary():
    print("=" * 65)
    print("           DJANGO FRAMEWORK - ƏSAS QAYDALAR XÜLASƏSİ")
    print("=" * 65)
    print("1. Django: Python-un 'Batteries Included' veb freymvorkudur.")
    print("2. MVT Arxitekturası: Model (Database), View (Logic), Template (UI).")
    print("3. Əsas fayllar: settings.py (konfiqurasiya), urls.py (marşrutlar).")
    print("4. Admin Panel: createsuperuser -> admin.py-də ModelAdmin özəlləşdirməsi.")
    print("5. CRUD & View Məntiqi: Create, Read, Update, Delete operatsiyaları.")
    print("6. Təhlükəsizlik & Yönləndirmə: CSRF token, redirect, reverse, request.GET.")
    print("7. Django Templates: {% extends %}, {% block %}, render(), teqlər və filtrlər.")
    print("=" * 65)


if __name__ == "__main__":
    show_django_summary()


