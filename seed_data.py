"""Seed script for UzWork — creates sample data for testing."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uzwork.settings')

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from accounts.models import User
from projects.models import Category, Project
from datetime import date, timedelta

# Create admin superuser
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@uzwork.uz',
        password='admin123',
        first_name='Admin',
        last_name='UzWork',
        role='admin'
    )
    print("Admin yaratildi: admin / admin123")

# Create sample client
if not User.objects.filter(username='buyurtmachi').exists():
    client = User.objects.create_user(
        username='buyurtmachi',
        email='client@uzwork.uz',
        password='test1234',
        first_name='Alisher',
        last_name='Karimov',
        role='client',
        phone='+998901234567',
        bio="IT kompaniya rahbari. Web va mobil ilovalar buyurtma qilaman.",
        location='Toshkent'
    )
    print("Buyurtmachi yaratildi: buyurtmachi / test1234")
else:
    client = User.objects.get(username='buyurtmachi')

# Create sample freelancers
freelancers_data = [
    {
        'username': 'frilanser1',
        'first_name': 'Sardor',
        'last_name': 'Raximov',
        'email': 'sardor@uzwork.uz',
        'skills': 'Python, Django, PostgreSQL, REST API',
        'bio': "5 yillik tajribaga ega backend dasturchi. Django va Python bo'yicha mutaxassis.",
        'location': 'Toshkent',
    },
    {
        'username': 'frilanser2',
        'first_name': 'Madina',
        'last_name': 'Azimova',
        'email': 'madina@uzwork.uz',
        'skills': 'React, JavaScript, HTML, CSS, Figma',
        'bio': "Frontend dasturchi va UI/UX dizayner. Zamonaviy veb-saytlar yarataman.",
        'location': 'Samarqand',
    },
    {
        'username': 'frilanser3',
        'first_name': 'Jasur',
        'last_name': 'Toshmatov',
        'email': 'jasur@uzwork.uz',
        'skills': 'Flutter, Dart, Firebase, Android, iOS',
        'bio': "Mobil dasturchi. Android va iOS ilovalar yarataman.",
        'location': 'Buxoro',
    },
    {
        'username': 'frilanser4',
        'first_name': 'Nilufar',
        'last_name': 'Saidova',
        'email': 'nilufar@uzwork.uz',
        'skills': 'Photoshop, Illustrator, Figma, Branding',
        'bio': "Grafik dizayner. Logotip, banner va brending xizmatlari.",
        'location': 'Toshkent',
    },
]

for fd in freelancers_data:
    if not User.objects.filter(username=fd['username']).exists():
        User.objects.create_user(
            username=fd['username'],
            email=fd['email'],
            password='test1234',
            first_name=fd['first_name'],
            last_name=fd['last_name'],
            role='freelancer',
            skills=fd['skills'],
            bio=fd['bio'],
            location=fd['location'],
            phone='+99890' + str(hash(fd['username']))[-7:],
        )
        print(f"Frilanser yaratildi: {fd['username']} / test1234")

# Create categories
categories_data = [
    ('Web dasturlash', 'web-dasturlash', '💻'),
    ('Mobil ilovalar', 'mobil-ilovalar', '📱'),
    ('Dizayn', 'dizayn', '🎨'),
    ('Marketing', 'marketing', '📣'),
    ('Tarjima', 'tarjima', '🌐'),
    ('Yozuv', 'yozuv', '✍️'),
    ('Video montaj', 'video-montaj', '🎬'),
    ('Ma\'lumotlar tahlili', 'data-tahlili', '📊'),
]

for name, slug, icon in categories_data:
    Category.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon})
print(f"{len(categories_data)} ta kategoriya yaratildi")

# Create sample projects
projects_data = [
    {
        'title': 'Onlayn do\'kon veb-sayti',
        'description': "E-commerce platforma yaratish kerak. Mahsulotlar katalogi, savatcha, to'lov tizimi va admin panel bo'lishi shart. React + Django texnologiyalari bilan. Responsive dizayn talab qilinadi.",
        'budget': 15000000,
        'deadline': date.today() + timedelta(days=30),
        'category_slug': 'web-dasturlash',
    },
    {
        'title': 'Restoran uchun mobil ilova',
        'description': "Restoran uchun buyurtma berish ilovasi. Menyu, buyurtma, to'lov, yetkazib berish kuzatish funksiyalari. Android va iOS uchun.",
        'budget': 20000000,
        'deadline': date.today() + timedelta(days=45),
        'category_slug': 'mobil-ilovalar',
    },
    {
        'title': 'Kompaniya logotipi va brending',
        'description': "Yangi startap uchun logotip, vizitka, brand-buk yaratish. Zamonaviy va minimalist uslubda.",
        'budget': 3000000,
        'deadline': date.today() + timedelta(days=14),
        'category_slug': 'dizayn',
    },
    {
        'title': 'CRM tizimi yaratish',
        'description': "Kichik biznes uchun CRM tizimi. Mijozlar bazasi, buyurtmalar, hisobotlar, xodimlar boshqaruvi. Django + PostgreSQL.",
        'budget': 25000000,
        'deadline': date.today() + timedelta(days=60),
        'category_slug': 'web-dasturlash',
    },
    {
        'title': 'SMM va reklama kampaniyasi',
        'description': "Instagram va Telegram uchun 1 oylik SMM strategiya va kontent-plan yaratish. Target reklama sozlash.",
        'budget': 5000000,
        'deadline': date.today() + timedelta(days=30),
        'category_slug': 'marketing',
    },
    {
        'title': 'Hujjatlarni ingliz tiliga tarjima',
        'description': "Texnik hujjatlar (50 bet) ni o'zbek tilidan ingliz tiliga professional tarjima qilish.",
        'budget': 2000000,
        'deadline': date.today() + timedelta(days=10),
        'category_slug': 'tarjima',
    },
]

for pd in projects_data:
    cat = Category.objects.filter(slug=pd['category_slug']).first()
    if not Project.objects.filter(title=pd['title']).exists():
        Project.objects.create(
            title=pd['title'],
            description=pd['description'],
            budget=pd['budget'],
            deadline=pd['deadline'],
            client=client,
            category=cat,
            status='open',
        )
        print(f"Loyiha yaratildi: {pd['title']}")

print("\n✅ Barcha namuna ma'lumotlar yaratildi!")
print("Admin: admin / admin123")
print("Buyurtmachi: buyurtmachi / test1234")
print("Frilanserlar: frilanser1-4 / test1234")
