"""
===============================================================================
                     DJANGO FRAMEWORK - ƏSAS QAYDALAR VƏ ANLAYIŞLAR
===============================================================================
Bu fayl Django Veb Freymvorkunun ümumi mahiyyətini, arxitekturasını (MVT), 
əsas əmrlərini, standart layihə strukturunu, Verilənlər Bazası (Database & ORM), 
İstifadəçi və Superuser (User & Auth), və Django Admin Panelinin qurulması, 
özəlləşdirilməsi qaydalarını aydın, səliqəli dildə izah edir.
===============================================================================
"""

try:
    import django
    from django.db import models
    from django.contrib.auth.models import User
    from django.contrib import admin
    from django.shortcuts import render, redirect
    from django.contrib.auth import authenticate, login, logout
    from django.contrib.auth.decorators import login_required
    from django.core.exceptions import PermissionDenied
except Exception:
    pass

# =============================================================================
# 1. DJANGO NƏDİR? (WHAT IS DJANGO?)
# =============================================================================

"""
1.1. ÜMUMİ TƏRİF
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
# 5. VERİLƏNLƏR BAZASI VƏ ORM (DATABASE & MODELS - `models.py`)
# =============================================================================

"""
5.1. QAYDALAR (RULES)
---------------------
1. Model Sinfinin Təyini:
   - Bütün verilənlər bazası obyektləri `django.db.models.Model` sinfindən irsiyyət almalıdır.
   - Hər bir model verilənlər bazasında bir cədvələ (table), modelin sahələri (fields) isə cədvəlin sütunlarına uyğundur.

2. Sahə Tipləri (Field Types):
   - Mətn üçün `CharField(max_length=...)` və ya böyük mətnlər üçün `TextField()`.
   - Ədədlər üçün `IntegerField()`, `FloatField()`, `DecimalField()`.
   - Tarix üçün `DateTimeField(auto_now_add=True)` (yaradılma vaxtı) və ya `auto_now=True` (son yenilənmə).
   - Məntiqi dəyər üçün `BooleanField(default=True/False)`.

3. Əlaqələr (Relationships):
   - Bir-Çoxa (1-to-N): `ForeignKey(TargetModel, on_delete=models.CASCADE, related_name="...")`.
   - Bir-Bura (1-to-1): `OneToOneField(TargetModel, on_delete=models.CASCADE)`.
   - Çox-Çoxa (N-to-N): `ManyToManyField(TargetModel)`.
   - `on_delete` opsiyaları: `CASCADE` (ana obyekt silinəndə bağlı obyektlər də silinsin), `SET_NULL` (silinəndə NULL qoyulsun), `PROTECT` (silinməyə icazə verilməsin).

4. Metodlar və Meta Sinfi:
   - `__str__(self)` metodu HƏMİŞƏ təyin olunmalıdır. Obyektin string təmsilini qaytarır.
   - `class Meta` daxilində `ordering = ['-created_at']`, `verbose_name`, `verbose_name_plural`, `db_table` tənzimlənir.

5. Səmərəli Sorğular (Optimization):
   - N+1 sorğu probleminin qarşısını almaq üçün `select_related()` (ForeignKey) və `prefetch_related()` (ManyToManyField) istifadə edilməlidir.

5.2. KOD NÜMUNƏSİ (`models.py`):
--------------------------------
```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kateqoriya Adı")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="products", 
        verbose_name="Kateqoriya"
    )
    title = models.CharField(max_length=200, verbose_name="Məhsul Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Təsvir")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Qiymət")
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"

    def __str__(self):
        return f"{self.title} - {self.price} AZN"

    def get_discounted_price(self, discount_percent: float) -> float:
        '''Biznes məntiqi: Model daxilində xüsusi metod'''
        return float(self.price) * (1 - discount_percent / 100)
```

5.3. MƏNTİQİ İZAH (LOGIC EXPLANATION):
--------------------------------------
- OBYEKT-YÖNÜMLÜ BAZA MÜHİTİ (ORM): Django Object-Relational Mapper (ORM) proqramçıya SQL 
  yazmadan (`SELECT * FROM product WHERE...`) sırf Python obyektləri və sinifləri ilə 
  verilənlər bazasını idarə etmək imkanı verir. Bu, həm kodun təhlükəsizliyini (SQL Injection-a qarşı), 
  həm də portativliyini (PostgreSQL, MySQL, SQLite arasında keçidi) təmin edir.

- `__str__` METODUNUN MƏNTİQİ: Əgər bu metod təyin olunmazsa, Django obyektləri 
  `<Product: Product object (1)>` kimi göstərər. `__str__` yazıldıqda isə obyektlər 
  admin panelində və ya CLI terminalında "iPhone 15 - 2000 AZN" kimi insan üçün anlaşılan şəkildə nümayiş olunur.

- `select_related` vs `prefetch_related` MƏNTİQİ: 
  Siyahıda 100 məhsul və onların kateqoriyası varsa, `Product.objects.all()` ilə hər məhsul üçün 
  ayrıca SQL sorğusu gedir (101 sorğu = N+1 problemi). `Product.objects.select_related('category').all()` 
  yazdıqda Django SQL `JOIN` edərək BÜTÜN məlumatı tək bir sorğu ilə bazadan çəkir.
"""


# =============================================================================
# 6. İSTİFADƏÇİ VƏ SUPERUSER İDARƏETMƏSİ (USER & AUTHENTICATION)
# =============================================================================

"""
6.1. QAYDALAR (RULES)
---------------------
1. Django Autentifikasiya Sistemi (`django.contrib.auth`):
   - Django daxilində hazır `User` modeli ilə gəlir (username, email, password, first_name, last_name).
   - Şifrələr bazada heç vaxt açıq (plain-text) saxlanılmır; `PBKDF2` alqoritmi ilə heşlənir.
   - İstifadəçiyə şifrə təyin edərkən `user.set_password('raw_password')` istifadə olunmalıdır.

2. Superuser (Super İstifadəçi) və Rollar:
   - Superuser sistemdə maksimum səlahiyyətə malik inzibatçıdır (`is_superuser=True`, `is_staff=True`).
   - Terminal vasitəsilə yaradılır: `python manage.py createsuperuser`
   - Staff User (`is_staff=True`): Admin panelinə girə bilən, lakin yalnız verilmiş icazələri icra edə bilən istifadəçi.
   - Sadə İstifadəçi (`is_staff=False`, `is_superuser=False`): Yalnız saytın daxili funksiyalarından istifadə edir.

3. Views və Giriş Təhlükəsizliyi:
   - Yalnız giriş etmiş istifadəçilərin keçə bildiyi view-lar `@login_required(login_url='login')` dekoratoru ilə qorunmalıdır.
   - Sorğu zamanı istifadəçinin daxil olub-olmadığı `request.user.is_authenticated` atributu ilə yoxlanılır.
   - Səlahiyyət yoxlanışı: `request.user.is_superuser` və ya `request.user.has_perm('app.perm')`.

6.2. KOD NÜMUNƏSİ (`views.py` & Auth Handling):
------------------------------------------------
```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

# 1. Giriş etmə View-u (Login Logic)
def user_login_view(request):
    if request.method == 'POST':
        username_val = request.POST.get('username')
        password_val = request.POST.get('password')
        
        # İstifadəçinin parolu və adının doğruluğunu yoxlayırıq:
        user = authenticate(request, username=username_val, password=password_val)
        if user is not None:
            login(request, user)  # Sessiya (Session) başladılır
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'İstifadəçi adı və ya parol yanlışdır!'})
            
    return render(request, 'login.html')

# 2. İstifadəçi Profil View-u (Qorunan Səhifə)
@login_required(login_url='login')
def profile_dashboard(request):
    # request.user vasitəsilə daxil olmuş istifadəçiyə çıxış əldə edirik:
    current_user = request.user
    user_products = current_user.products.all() if hasattr(current_user, 'products') else []
    
    return render(request, 'dashboard.html', {
        'user': current_user,
        'products': user_products
    })

# 3. Yalnız Superuser üçün İdarəetmə Səhifəsi
@login_required
def superuser_admin_panel(request):
    if not request.user.is_superuser:
        # İcazəsi olmayan istifadəçiyə 403 Forbidden xətası verir
        raise PermissionDenied("Bu səhifəyə daxil olmaq üçün Superuser səlahiyyəti lazımdır!")
    
    total_users = User.objects.count()
    return render(request, 'superuser_panel.html', {'total_users': total_users})

# 4. Çıxış etmə View-u (Logout Logic)
def user_logout_view(request):
    logout(request)  # Sessiya məhv edilir
    return redirect('login')
```

6.3. MƏNTİQİ İZAH (LOGIC EXPLANATION):
--------------------------------------
- `authenticate()` METODUNUN MƏNTİQİ: Daxil edilən düz mətni (plain-text password) 
  verilənlər bazasındakı heşlənmiş parol ilə müqayisə edir. Şifrələr eyni olduqda `User` 
  obyektini qaytarır, əks halda `None` qaytarır. Bu, şifrələrin təhlükəsizliyini 100% təmin edir.

- SESSİYA (SESSION) VƏ COOKIE MƏNTİQİ: `login(request, user)` çağırıldıqda Django 
  server tərəfdə unikal bir session ID yaradır və brauzerə `sessionid` adlı cookie göndərir. 
  Hər növbəti sorğuda `request.user` avtomatik olaraq həmin cookie vasitəsilə tapılır.

- SƏLAHİYYƏT (AUTHORIZATION) İZAHI: Autentifikasiya "İstifadəçi kimdir?" sualına, 
  Avtorizasiya (Səlahiyyət) isə "Bu istifadəçi nəyi edə bilər?" sualına cavab verir. 
  `@login_required` istifadəçinin daxil olub-olmadığını, `is_superuser` isə onun inzibatçı 
  səlahiyyətinə malik olub-olmadığını yoxlayır.
"""


# =============================================================================
# 7. DJANGO ADMİN PANELİ VƏ ÖZƏLLƏŞDİRİLMƏSİ (`admin.py`)
# =============================================================================

"""
7.1. QAYDALAR (RULES)
---------------------
1. Qeydiyyat Metodları:
   - Metod A: `admin.site.register(ModelName)` (Sadə qeydiyyat).
   - Metod B: `@admin.register(ModelName)` + `class ModelNameAdmin(admin.ModelAdmin)` (Peşəkar və özəlləşdirilmiş).

2. Siyahı Görünüşünün Konfiqurasiyası (`ModelAdmin` Atributları):
   - `list_display`: Cədvəldə nümayiş olunacaq sütunlar `('id', 'title', 'price', 'created_at')`.
   - `list_display_links`: Kliklədikdə redaktə səhifəsinə aparan sütunlar `('id', 'title')`.
   - `list_filter`: Sağ yan paneldə filtrləmə paneli yaradır `('is_active', 'category', 'created_at')`.
   - `search_fields`: Axtarış sahəsi aktivləşdirir `('title', 'description', 'category__name')`.
   - `list_editable`: Siyahıdan birbaşa dəyişdirilə bilən sahələr `('price', 'is_active')`.
   - `readonly_fields`: Redaktə edilə bilinməyən, yalnız oxunan sahələr `('created_at',)`
   - `list_per_page`: Bir səhifədə göstəriləcək element sayı `(default: 100)`.
   - `ordering`: İlkin sıralama parametri `('-created_at',)`

3. Xüsusi Sütunlar və Actions:
   - `@admin.display(description="...", boolean=True)` dekoratoru ilə model metodlarını və ya custom funksiyaları admin cədvəlinə sütun kimi əlavə etmək olar.
   - Toplu əməliyyatlar üçün `actions = [make_published, export_as_csv]` yazılır.

4. İçi-içə Admin İdarəetməsi (Inline Admin):
   - Ana model ilə bağlı alt modelləri (məsələn, Sifariş daxilində Sifariş Məhsulları) eyni səhifədə redaktə etmək üçün `TabularInline` və ya `StackedInline` istifadə olunur.

7.2. KOD NÜMUNƏSİ (`admin.py`):
--------------------------------
```python
from django.contrib import admin
from .models import Category, Product

# 1. Inline Admin (Product-ları Category səhifəsində göstərmək üçün)
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # Müvəqqəti əlavə olunacaq boş sətr sayı
    fields = ('title', 'price', 'is_active')

# 2. Kateqoriya Admin Tənzimlənməsi
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'product_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # Ad yazıldıqca avtomatik slug yaradır
    inlines = [ProductInline]

    @admin.display(description="Məhsul Sayı")
    def product_count(self, obj):
        return obj.products.count()

# 3. Məhsul Admin Tənzimlənməsi
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Siyahıda görünəcək sütunlar:
    list_display = ('id', 'title', 'category', 'price', 'is_active', 'created_at', 'status_badge')
    
    # Redaktə linkləri:
    list_display_links = ('id', 'title')
    
    # Sağ tərəfdə filtrləmə paneli:
    list_filter = ('is_active', 'category', 'created_at')
    
    # Axtarış sətiri (Category modelinin name sahəsində də axtarır):
    search_fields = ('title', 'description', 'category__name')
    
    # Birbaşa siyahıda dəyişdirilə bilən sahələr:
    list_editable = ('price', 'is_active')
    
    # Səhifələmə:
    list_per_page = 25
    
    # Yalnız oxunabilən sahələr:
    readonly_fields = ('created_at',)
    
    # Sıralama:
    ordering = ('-created_at',)
    
    # Toplu Admin Əməliyyatları (Custom Action)
    actions = ['make_deactive', 'make_active']

    @admin.action(description="Seçilmiş məhsulları qeyri-aktiv et")
    def make_deactive(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(request, f"{updated_count} məhsul uğurla qeyri-aktiv edildi.")

    @admin.action(description="Seçilmiş məhsulları aktiv et")
    def make_active(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(request, f"{updated_count} məhsul uğurla aktiv edildi.")

    @admin.display(description="Status", boolean=True)
    def status_badge(self, obj):
        return obj.is_active
```

7.3. MƏNTİQİ İZAH (LOGIC EXPLANATION):
--------------------------------------
- `ModelAdmin` SİNFİNİN MƏNTİQİ: Django Admin standart olaraq yalnız obyektləri sadalayır. 
  `ModelAdmin` sinfi admin panelin davranışını tam nəzarətə almağa imkan verir. Kod təkrarı olmadan 
  inzibatçı üçün axtarış, filtrləmə və sıralama kimi mürəkkəb interfeysləri cəmi 5-10 sətir kodla yaradır.

- `category__name` AXTARIŞ SİNTAKSİSİ: Axtarış sahəsində `category__name` yazıldıqda 
  Django ORM xarici açara (ForeignKey) sahib `Category` cədvəlinə avtomatik SQL JOIN sorğusu atır. 
  Beləliklə məhsul axtararkən onun kateqoriya adını daxil etsək belə nəticələr dərhal tapılır.

- CUSTOM ACTION MƏNTİQİ: Minlərlə məhsulu tək-tək açıb `is_active=False` etmək saatlar ala bilər. 
  Custom Action metodları bazaya tək bir `UPDATE product SET is_active=False WHERE id IN (...)` 
  sorğusu göndərərək bütün seçilmiş obyektləri 1 millisaniyədə yeniləyir.
"""


# =============================================================================
# 8. CRUD ƏMƏLİYYATLARI VƏ VIEW MƏNTİQİ (KNOWLEDGE HUB PRAKTİKASI)
# =============================================================================

"""
8.1. CRUD NƏDİR?
----------------
CRUD — Veb tətbiqlərdə verilənlər üzərində aparılan 4 əsas əməliyyatdır:
- C (Create)  : Yeni obyekt yaradılması (`note_create` funksiyası).
- R (Read)    : Obyektlərin siyahısı və detal baxışı (`notes_list`, `note_detail`).
- U (Update)  : Mövcud obyektin redaktə olunması (`note_edit` funksiyası).
- D (Delete)  : Obyektin sistemdən silinməsi (`note_delete` funksiyası).

8.2. KRİTİK DJANGO FUNKSİYALARI VƏ ANLAYIŞLARI
----------------------------------------------

1. `CSRF Qorunması (Cross-Site Request Forgery - Dərin İzah)`:
   a) CSRF Hücumu Nədir? Zərərli 3-cü tərəf saytı, istifadəçinin brauzerində aktiv olan sessiyadan 
      istifadə edərək icazəsiz sorğu göndərir.
   b) Django Necə Qoruyur? Django daxili `CsrfViewMiddleware` vasitəsilə gizli bir token 
      göndərilməsini tələb edir və brauzerdəki cookie ilə müqayisə edir.

2. `redirect("route_name", **kwargs)`:
   - POST sorğusundan sonra istifadəçini başqa səhifəyə yönləndirir (PRG Pattern).

3. `reverse("route_name", kwargs={"id": 1})`:
   - URL-in adından istifadə edərək marşrut ünvanını dinamik generasiya edir.

4. `request.GET.get("param")` & Dinamik Filtrləmə:
   - URL query parametrlərini (`/notes/?tag=python`) oxuyur.
"""


# =============================================================================
# 9. DJANGO TEMPLATES ARXİTEKTURASI VƏ İRSİLİK (TEMPLATES & INHERITANCE)
# =============================================================================

"""
9.1. TEMPLATES NƏDİR VƏ STRUKTURU
----------------------------------
Django Templates — Python məntiqi ilə HTML interfeysini ayıran dinamik şablonlaşdırma sistemidir.

9.2. ƏSAS TEMPLATE TEQLƏRİ VƏ FİLTRLƏRİ
---------------------------------------
- `{% extends "base.html" %}` : Ana şablondan irsilik alır.
- `{% block content %} ... {% endblock %}` : Doldurulacaq dinamik blok.
- `{% include "includes/nav.html" %}` : Komponent əlavə edir.
- `{{ value|upper }}`, `{{ value|date:"d.m.Y" }}`, `{{ value|default:"Boşdur" }}`
"""


# =============================================================================
# 10. QISA XÜLASƏ ÇAPI
# =============================================================================

def show_django_summary():
    print("=" * 70)
    print("           DJANGO FRAMEWORK - ƏSAS QAYDALAR VƏ ANLAYIŞLAR")
    print("=" * 70)
    print("1. Django MVT: Model (Database), View (Business Logic), Template (UI).")
    print("2. Database & ORM: models.Model, ForeignKey, select_related, __str__.")
    print("3. Auth & User: User, Superuser (createsuperuser), login, @login_required.")
    print("4. Admin Panel: @admin.register, ModelAdmin (list_display, list_filter, search_fields).")
    print("5. CRUD & Security: Create/Read/Update/Delete, CSRF token, PRG Pattern.")
    print("6. Templates: {% extends %}, {% block %}, {% include %}, teqlər və filtrlər.")
    print("=" * 70)


if __name__ == "__main__":
    show_django_summary()
