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
# 6. QISA XÜLASƏ ÇAPI
# =============================================================================

def show_django_summary():
    print("=" * 65)
    print("           DJANGO FRAMEWORK - ƏSAS QAYDALAR XÜLASƏSİ")
    print("=" * 65)
    print("1. Django: Python-un 'Batteries Included' veb freymvorkudur.")
    print("2. MVT Arxitekturası: Model (Database), View (Logic), Template (UI).")
    print("3. Əsas fayllar: settings.py (konfiqurasiya), urls.py (marşrutlar).")
    print("4. Admin Panel: createsuperuser -> admin.py-də ModelAdmin özəlləşdirməsi.")
    print("5. İş axını: URL -> View -> Model/Data -> HttpResponse.")
    print("=" * 65)


if __name__ == "__main__":
    show_django_summary()
