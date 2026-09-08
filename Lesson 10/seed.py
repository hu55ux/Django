import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Product, Review

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created superuser: admin / admin123")

# Create test users if not exist
if not User.objects.filter(username='john_doe').exists():
    user1 = User.objects.create_user('john_doe', 'john@example.com', 'pass1234')
    print("Created user: john_doe / pass1234")
else:
    user1 = User.objects.get(username='john_doe')

if not User.objects.filter(username='jane_smith').exists():
    user2 = User.objects.create_user('jane_smith', 'jane@example.com', 'pass1234')
    print("Created user: jane_smith / pass1234")
else:
    user2 = User.objects.get(username='jane_smith')

# Sample Products
products_data = [
    {
        "name": "Wireless Noise-Canceling Headphones",
        "description": "Experience crystal clear acoustics and deep bass with premium active noise cancellation and up to 30 hours of battery life."
    },
    {
        "name": "Ergonomic Mechanical Keyboard",
        "description": "Custom tactile switches with customizable RGB backlighting and an aircraft-grade aluminum frame for ultimate typing comfort."
    },
    {
        "name": "Ultra HD 4K Gaming Monitor 27\"",
        "description": "144Hz refresh rate with 1ms response time and HDR400 support. Perfect for competitive gaming and content creation."
    },
    {
        "name": "Smart Fitness Watch Series X",
        "description": "Tracks heart rate, sleep metrics, GPS navigation, and blood oxygen levels with 50m water resistance and crisp OLED display."
    }
]

for p_data in products_data:
    p, created = Product.objects.get_or_create(
        name=p_data["name"],
        defaults={"description": p_data["description"]}
    )
    if created:
        print(f"Created product: {p.name}")

# Sample Reviews
p1 = Product.objects.get(name="Wireless Noise-Canceling Headphones")
p2 = Product.objects.get(name="Ergonomic Mechanical Keyboard")

if not Review.objects.filter(product=p1, user=user1).exists():
    Review.objects.create(
        product=p1,
        user=user1,
        text="Absolutely amazing sound quality! The active noise cancellation completely blocks out background noise when working in noisy cafes.",
        rating=5
    )
    print("Added review for Headphones by john_doe")

if not Review.objects.filter(product=p1, user=user2).exists():
    Review.objects.create(
        product=p1,
        user=user2,
        text="Great battery life and very comfortable ear cushions. Bluetooth connection connects instantly every time.",
        rating=4
    )
    print("Added review for Headphones by jane_smith")

if not Review.objects.filter(product=p2, user=user1).exists():
    Review.objects.create(
        product=p2,
        user=user1,
        text="Solid build quality and typing feels super responsive. Highly recommended for programmers!",
        rating=5
    )
    print("Added review for Keyboard by john_doe")

print("Seeding completed successfully!")
