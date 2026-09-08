# Django Forms, Templates, Views, Database, Auth və Admin Qaydaları (Best Practices)

Bu sənəd Django proqramlarında Formlar (`forms.py`), Görüntülər (`views.py`), Şablonlar (`templates`), Verilənlər Bazası (`models.py`), İstifadəçi İdarəetməsi (`User/Superuser`) və Admin Paneli (`admin.py`) üçün müəyyən edilmiş əsas qaydaları, kod nümunələrini və onların məntiqi izahını ehtiva edir.

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
   - Form keçərsiz olduqda və ya biznes məntiqində xəta baş verdikdə (`form.add_error(None, message)`), form obyekti eyni şablona ötürülərək istifadəçiyə xətalar göstərilməlidir.

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

## 4. Verilənlər Bazası və ORM (`models.py`) Qaydaları

1. **Model Strukturunun Təyin Edilməsi:**
   - Bütün verilənlər bazası obyektləri `models.Model` sinfindən törəməlidir.
   - Hər bir modeldə obyektin oxunaqlı təmsilini verən `__str__(self)` metodu mütləq təyin olunmalıdır.
   - İndeksləmə, sıralama və adlandırma üçün `Meta` sinfindən istifadə edilməlidir.

2. **Əlaqələr (Relationships) və İlişkilər:**
   - Bir-çoxa əlaqələr üçün `ForeignKey`, bir-bura əlaqələr üçün `OneToOneField`, çox-çoxa əlaqələr üçün `ManyToManyField` istifadə olunur. `on_delete` parametri (məsələn, `models.CASCADE` və ya `models.SET_NULL`) mütləq göstərilməlidir.

3. **Verilənlər Bazası Miqrasiyaları (Migrations):**
   - Modeldə edilən hər bir dəyişiklikdən sonra `python manage.py makemigrations` (miqrasiya faylının yaradılması) və `python manage.py migrate` (baza strukturunun yenilənməsi) icra edilməlidir.

4. **Səmərəli Sorğular (ORM Optimization):**
   - N+1 sorğu probleminin qarşısını almaq üçün xarici açarlı əlaqələrdə `select_related()` (ForeignKey/OneToOne) və `prefetch_related()` (ManyToManyField) metodlarından istifadə olunmalıdır.

### Nümunə Kod (`models.py`):
```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya Adı")

    class Meta:
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    movie_title = models.CharField(max_length=200)
    seat_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie_title} (Oturacaq: {self.seat_number})"

    def is_recent(self):
        """Biznes məntiqi: Model daxilində yazılan metod"""
        from django.utils import timezone
        return (timezone.now() - self.created_at).days < 1
```

### Məntiqi İzah:
- **Modellər verilənlər bazasındakı cədvəllərin obyekt yönümlü (ORM) təmsilidir.** Birbaşa SQL yazmaq əvəzinə Python kodları vasitəsilə verilənlər bazası ilə təhlükəsiz qarşılıqlı əlaqə qurulur.
- **`__str__` metodu:** Admin panelində və CLI/Shell-də obyektlərin `Ticket object (1)` kimi deyil, oxunaqlı şəkildə (`user - film - seat`) görünməsini təmin edir.
- **`select_related` / `prefetch_related`:** Baza sorğularının sayını azaltmaqla tətbiqin sürətini və performansını dəfələrlə artırır.

---

## 5. İstifadəçi və Superuser (User / Auth) Qaydaları

1. **Autentifikasiya və İstifadəçi İdarəetməsi:**
   - Django hazır `django.contrib.auth` sistemini təqdim edir. İstifadəçilərin şifrələri verilənlər bazasında heç vaxt açıq (plain-text) saxlanılmır, avtomatik olaraq heşlənir (`PBKDF2/SHA256`).

2. **Superuser (Super İstifadəçi) Yaradılması:**
   - Bütün sistemə, admin panelinə və bütün məlumatlara tam giriş hüququ olan superuser terminal əmri ilə yaradılır:
     ```bash
     python manage.py createsuperuser
     ```
   - Superuser atributları: `is_superuser=True`, `is_staff=True`, `is_active=True`.

3. **Görüntülərdə Giriş Məhdudiyyəti və Səlahiyyətlər (Permissions):**
   - Yalnız giriş etmiş istifadəçilərin daxil ola biləcəyi görüntülər `@login_required` dekoratoru və ya `LoginRequiredMixin` ilə qorunmalıdır.
   - İstifadəçinin rolu `request.user.is_staff` (admin personalı) və ya `request.user.is_superuser` (tam sistem inzibatçısı) ilə yoxlanılır.

### Nümunə Kod (`views.py`):
```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

@login_required
def profile_view(request):
    """Yalnız giriş etmiş istifadəçilər görə bilər"""
    user_tickets = request.user.tickets.all()  # related_name vasitəsilə istifadəçinin biletləri
    return render(request, 'profile.html', {'tickets': user_tickets})

def admin_only_dashboard(request):
    """Yalnız superuser və ya staff daxil ola bilər"""
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        raise PermissionDenied("Bu səhifəyə yalnız Superuser daxil ola bilər!")
    
    return render(request, 'admin_dashboard.html')
```

### Məntiqi İzah:
- **Təhlükəsizlik (Security):** İstənilən mühüm əməliyyatdan (bilet almaq, profil yeniləmək) öncə `request.user.is_authenticated` yoxlanmalıdır. Bu, anonim istifadəçilərin icazəsiz data dəyişdirməsinin qarşısını alır.
- **Superuser və Staff Fərqi:** `is_staff=True` istifadəçiyə admin panelinə girməyə icazə verir, `is_superuser=True` isə heç bir məhdudiyyət olmadan bütün model və icazələrə sahib olur.

---

## 6. Admin Paneli (`admin.py`) Qaydaları

1. **Modellərin Admin Panelində Qeydiyyatı:**
   - Admin panelində idarə olunacaq hər bir model `admin.site.register(ModelName, CustomAdmin)` və ya `@admin.register(ModelName)` dekoratoru ilə qeydə alınmalıdır.

2. **Admin Görünüşünün Tənzimlənməsi (`ModelAdmin`):**
   - **`list_display`**: Cədvəl görünüşündə hansı sütunların nümayiş etdiriləcəyini müəyyən edir.
   - **`list_filter`**: Sağ tərəfdə filtrləmə panelini (məsələn, tarixə, kateqoriyaya görə) aktivləşdirir.
   - **`search_fields`**: Axtarış qutusunu aktivləşdirir və axtarılacaq sahələri təyin edir (məsələn, `['movie_title', 'user__username']`).
   - **`ordering`**: İlkin sıralamanı müəyyən edir.
   - **`readonly_fields`**: Yalnız oxunabilən (dəyişdirilə bilməyən) sahələri göstərir.

3. **Xüsusi Action-lar (Custom Admin Actions):**
   - Toplu əməliyyatları həyata keçirmək üçün admin sinfi daxilində xüsusi action metodları yazılır.

### Nümunə Kod (`admin.py`):
```python
from django.contrib import admin
from .models import Category, Ticket

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Siyahıda görünəcək sütunlar
    list_display = ('id', 'user', 'movie_title', 'seat_number', 'created_at', 'is_recent_ticket')
    
    # Filtrləmə paneli
    list_filter = ('created_at', 'movie_title')
    
    # Axtarış sahələri (ForeignKey üçün user__username istifadə olunur)
    search_fields = ('movie_title', 'user__username', 'user__email')
    
    # Düzəliş edilə bilməyən sahələr
    readonly_fields = ('created_at',)
    
    # Siyahıda default sıralama
    ordering = ('-created_at',)
    
    # Custom metodun admin panelində sütun kimi göstərilməsi
    @admin.display(description="Yeni Bilet?", boolean=True)
    def is_recent_ticket(self, obj):
        return obj.is_recent()
```

### Məntiqi İzah:
- **İdarəetmə Asanlığı (Usability):** Standart Django admin modeli sadəcə obyektin adını göstərir. `list_display`, `list_filter` və `search_fields` əlavə etməklə minlərlə məlumat arasından lazımi bileti və ya istifadəçini saniyələr daxilində tapmaq və idarə etmək mümkün olur.
- **ForeignKey Axtarışı:** Axtarış sahəsində `user__username` yazmaqla Django ORM avtomatik olaraq SQL `JOIN` əməliyyatı apararaq bilet sahibi olan istifadəçinin adı üzrə axtarış edir.

---

## 7. Test və Yoxlama Qaydaları

- Dəyişikliklərdən sonra sistem yoxlaması:
  ```bash
  python manage.py check
  ```
- Verilənlər bazası miqrasiya statusunu yoxlamaq:
  ```bash
  python manage.py showmigrations
  ```
- Unit testlərin icrası:
  ```bash
  python manage.py test
  ```
