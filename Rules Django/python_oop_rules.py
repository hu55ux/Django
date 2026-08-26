"""
===============================================================================
     PYTHON HƏRTƏRƏFLİ VƏ ƏTRAFLI QAYDALARİ (TYPES, COLLECTIONS & OOP)
===============================================================================
Bu fayl Python proqramlaşdırma dilinin BÜTÜN əsas anlayışlarını:
1. Məlumat Tipləri (Types), Mutability/Immutability, Slicing, Comprehensions
2. `collections` Modulunun strukturları (defaultdict, Counter, deque, namedtuple)
3. Xəta İdarəetməsi (Exception Handling: try/except/finally/custom exceptions)
4. Fayllarla İş və Kontekst Menecerləri (Context Managers: with statement)
5. Modullar, Paketlər və `__name__ == '__main__'`
6. Qabaqcıl Funksiyalar (Scope, Closure, Decorators, Generators)
7. Obyektə Yönəlmiş Proqramlaşdırma (OOP) və Sehrli (Dunder) Metodlar
bölmələrini ətraflı qaydalar və kodu nümayiş etdirən canlı misallarla izah edir.
===============================================================================
"""

from collections import defaultdict, Counter, deque, namedtuple
from typing import Any


# =============================================================================
# 1. MƏLUMAT TİPLƏRİ, MUTABILITY, SLICING VƏ COMPREHENSIONS
# =============================================================================

"""
1.1. MUTABLE vs IMMUTABLE (DƏYİŞDİRİLƏ BİLƏN VƏ BİLMƏYƏN TİPLƏR)
--------------------------------------------------------------
- Immutable (Dəyişdirilə BİLMƏYƏN): `int`, `float`, `str`, `tuple`, `bool`, `bytes`, `frozenset`.
  Bu tiplərin dəyəri yaddaşda dəyişdirilmir, yenisi yaradılır.
- Mutable (Dəyişdirilə BİLƏN): `list`, `dict`, `set`, `bytearray`.
  Bu tiplərin daxili dəyərləri eyni yaddaş ünvanında yenilənə bilir.

1.2. SLICING (DİLİMLƏMƏ ƏMƏLİYYATI)
------------------------------------
Qayda: `sequence[start:stop:step]`
- `start`: Başlanğıc indeksi (daxildir)
- `stop`: Bitiş indeksi (daxil DEYİL)
- `step`: Addım sayı (mənfi olduqda geriyə çevirir)
"""
text = "PythonDjango"
substring = text[0:6]     # "Python"
reversed_text = text[::-1] # "ognajDnohtyP"


"""
1.3. COMPREHENSIONS (SİYAHI, LÜĞƏT VƏ ÇOXLUQ ANLAYIŞLARI)
---------------------------------------------------------
Qayda: Dövr və şərtləri bir sətirdə yazaraq yeni kolleksiya yaradan sürətli sintaksis.
"""
# List Comprehension
squares: list[int] = [x**2 for x in range(10) if x % 2 == 0]  # [0, 4, 16, 36, 64]

# Dict Comprehension
char_count: dict[str, int] = {char: len(char * 2) for char in "abc"}  # {'a': 2, 'b': 2, 'c': 2}

# Set Comprehension
unique_lengths: set[int] = {len(w) for w in ["apple", "banana", "kiwi", "apple"]}  # {5, 6, 4}


# =============================================================================
# 2. `collections` MODULU STRUKTURLARI (ADVANCED COLLECTIONS)
# =============================================================================

"""
Python-un standart `collections` modulu daxili tiplərdən (list, dict, tuple) 
daha sürətli və funksional strukturlar təqdim edir:

1. `defaultdict`: Olmayan açara müraciət edildikdə KeyError vermir, defolt dəyər yaradır.
2. `Counter`: Obyektlərin sayını hesablayaraq hash-cədvəl (dict) şəklində saxlayır.
3. `deque` (Double-Ended Queue): Həm əvvəldən, həm sondan O(1) vaxtında element əlavə etmək/silmək.
4. `namedtuple`: İndekslə yanaşı sahə adları ilə müraciət olunan kortej.
"""

def demonstrate_collections():
    # 1. defaultdict
    dd: dict[str, list[int]] = defaultdict(list)
    dd["fruits"].append("Apple")  # KeyError vermir, birbaşa list yaradıb əlavə edir

    # 2. Counter
    counts = Counter(["apple", "banana", "apple", "orange", "apple"])
    # counts -> Counter({'apple': 3, 'banana': 1, 'orange': 1})

    # 3. deque
    dq = deque([1, 2, 3])
    dq.appendleft(0)  # Əvvələ əlavə edir -> deque([0, 1, 2, 3])
    dq.pop()          # Sondan silir -> 3

    # 4. namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(x=10, y=20)
    # p.x -> 10, p.y -> 20


# =============================================================================
# 3. XƏTA İDARƏETMƏSİ (EXCEPTION HANDLING)
# =============================================================================

"""
Qayda:
- `try`: Xəta baş verə biləcək kod bloku.
- `except`: Müəyyən xəta baş verdikdə icra olunan blok.
- `else`: Xəta BAŞ VERMƏDİKDƏ icra olunur.
- `finally`: Xəta olub-olmamasından asılı olmayaraq HƏMİŞƏ icra olunur (təmizlik işləri üçün).
- Xüsusi Xətalar (Custom Exceptions): `Exception` sinfindən irsiyyət alaraq yaradılır.
"""

class InvalidAgeError(Exception):
    """Yaş mənfi və ya həddən artıq böyük olduqda fırladılan xüsusi xəta."""
    pass


def validate_user_age(age: int) -> bool:
    if age < 0 or age > 120:
        raise InvalidAgeError(f"Keçərsiz yaş dəyəri: {age}")
    return True


def safe_divide(a: float, b: float) -> float:
    try:
        result = a / b
    except ZeroDivisionError as e:
        print(f"Xəta: Sıfıra bölməyə icazə verilmir! ({e})")
        return 0.0
    else:
        print("Bölmə əməliyyatı uğurla icra olundu.")
        return result
    finally:
        print("Əməliyyat tamamlandı (finally).")


# =============================================================================
# 4. FAYLLARLA İŞ VƏ KONTEKST MENECERLƏRİ (CONTEXT MANAGERS & WITH)
# =============================================================================

"""
Qayda:
- Fayl açıldıqdan sonra mütləq bağlanmalıdır.
- `with` ifadəsi (Context Manager) resursların (fayl, db qoşulması) avtomatik 
  bağlanmasını təmin edir (`__enter__` və `__exit__` metodları ilə).

Nümunə:
"""
class CustomResource:
    """Xüsusi Context Manager yaratmaq nümunəsi."""
    def __enter__(self):
        print("[Context] Resurs ayrıldı və hazırladı.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[Context] Resurs avtomatik olaraq təmizləndi və bağlandı.")
        return False  # Xətaları udmur, yuxarı fırladır


# =============================================================================
# 5. MODULLAR, PAKETLƏR VƏ __name__ == "__main__"
# =============================================================================

"""
Qayda:
- Modul: `.py` uzantılı tək bir Python faylıdır.
- Paket: İçərisində `__init__.py` faylı olan və modulları bir araya toplayan papkadır.
- `__name__ == "__main__"`: Fayl birbaşa icra olunduqda `__name__` dəyəri `"__main__"` olur.
  Fayl başqa modula `import` edildikdə isə icra olunmur.
"""


# =============================================================================
# 6. FUNKSİYALAR, SCOPE (LEGB), CLOSURE, DECORATORS VƏ GENERATORS
# =============================================================================

"""
6.1. LEGB SCOPE QAYDASI
-----------------------
Python dəyişəni 4 səviyyədə axtarır:
L - Local (Funksiya daxili)
E - Enclosing (Xarici funksiya daxili - closure)
G - Global (Modul səviyyəsində)
B - Built-in (Python-un hazır daxili funksiya/tipləri)

6.2. CLOSURE (QAPANMA)
----------------------
Daxili funksiya xarici funksiyanın mühitini yadda saxlayır.
"""
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment


"""
6.3. DECORATORS (@)
-------------------
Funksiyanın mənbə kodunu dəyişmədən ona funksionallıq elavə edir.
"""
def timer_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} İcra müddəti: {end - start:.4f} saniyə")
        return res
    return wrapper


"""
6.4. GENERATORS (YIELD)
-----------------------
Məlumatı yaddaşa doldurmadan hissə-hissə istehsal edən funksiya.
"""
def fibonacci(limit: int):
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b


"""
6.5. KEYWORD-ONLY ARGUMENTS (`*` PARAMETRİ)
-------------------------------------------
Funksiya parametr siyahısında tək başınalıq `*` simvolunun yazılması, 
həmin `*`-dan sonra gələn BÜTÜN arqumentlərin MÜTLƏQ adları ilə (Keyword Arguments) 
ötürülməsini tələb edir (Mövqeli / Positional arqument kimi ötürməyə icazə vermir).

Məqsədi:
- Kodu çağırarkən nəyin nə üçün ötürüldüyünü aydın göstərmək (Code Readability).
- Parametrlərin ardıcıllığını səhv salmaq riskini sıfıra endirmək.

Nümunə:
def create_note(*, title: str, body: str):
    return {"title": title, "body": body}

# ❌ SƏHV İSTİFADƏ (TypeError fırladır):
# create_note("Django", "Body text")

# ✅ DÜZGÜN İSTİFADƏ:
# create_note(title="Django", body="Body text")
"""


# =============================================================================
# 7. OOP-NİN ƏSAS SÜTUNLARI VƏ SEHRLİ METODLAR
# =============================================================================

"""
7.1. OOP SÜTUNLARI:
- Enkapsulyasiya: Dəyişənlərin və məntiqin qorunması.
- İrsiyyət: Siniflərin bir-birindən xüsusiyyət götürməsi (`super()`).
- Polimorfizm: Eyni adlı metodun fərqli siniflərdə fərqli işləməsi.

7.2. SEHRLİ (DUNDER) METODLAR:
-------------------------------------------------------------------------------
| Metod          | İzahı                                                     |
-------------------------------------------------------------------------------
| __init__       | Konstruktor - obyekti başlanğıc vəziyyətinə gətirir.       |
| __str__        | `str(obj)` və ya `print(obj)` zamanı oxunaqlı yazı qaytarır.|
| __bool__       | `bool(obj)` çağırılanda mənfi/müsbət olduğunu bildiri.     |
| __len__        | `len(obj)` çağırılanda ölçü dəyəri qaytarır.              |
| __lt__ (<)     | İki obyekti kiçikdir (<) operatoru ilə müqayisə edir.      |
| __eq__ (==)    | İki obyektin bərabərliyini yoxlayır.                       |
| __add__ (+)    | (+) operatoru ilə iki obyekti birləşdirir.                |
-------------------------------------------------------------------------------
"""

class Character:
    def __init__(self, name: str, health: int, attack_power: int):
        self.name = name
        self.health = max(0, health)
        self.attack_power = attack_power

    def __str__(self) -> str:
        return f"Qəhrəman: {self.name} | HP: {self.health}"

    def __bool__(self) -> bool:
        return self.health > 0

    def __len__(self) -> int:
        return self.health

    def __lt__(self, other) -> bool:
        if not isinstance(other, Character):
            return NotImplemented
        return self.health < other.health

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Character):
            return False
        return self.name == other.name and self.health == other.health

    def __add__(self, other):
        if isinstance(other, Character):
            return f"Komanda: {self.name} və {other.name}"
        return NotImplemented


# =============================================================================
# 8. QISA XÜLASƏ ÇAPI
# =============================================================================

def print_full_rules_summary():
    print("=" * 70)
    print("      PYTHON BÜTÜN ƏSAS ANLAYIŞLAR VƏ OOP - QAYDALAR XÜLASƏSİ")
    print("=" * 70)
    print("1. Tiplər & Slicing: Mutable vs Immutable, Comprehensions, Dilimləmə.")
    print("2. collections Modulu: defaultdict, Counter, deque, namedtuple.")
    print("3. Xəta İdarəsi: try, except, else, finally, raise, Custom Errors.")
    print("4. Resurslar: with operatoru (Context Manager) və fayllarla iş.")
    print("5. Qabaqcıl Məntiq: Scope (LEGB), Closure, Decorator (@), Generator (yield).")
    print("6. OOP: Enkapsulyasiya, İrsiyyət, Polimorfizm, Dunder Metodlar.")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_collections()
    safe_divide(10, 2)
    print_full_rules_summary()
