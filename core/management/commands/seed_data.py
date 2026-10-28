"""Populate the database with realistic demo data.

Usage:  python manage.py seed_data
"""
import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Profile
from billing.models import Bill, BillItem
from core.models import GalleryImage, RestaurantSetting, Testimonial
from customers.models import Customer
from kitchen.models import Order, OrderItem
from menu.models import Category, MenuItem
from reservations.models import Reservation
from tables.models import RestaurantTable

U = "https://images.unsplash.com/"

CATEGORIES = [
    ("Pizza", "fa-solid fa-pizza-slice", f"{U}photo-1513104890138-7c749659a591?w=400&q=80"),
    ("Burger", "fa-solid fa-burger", f"{U}photo-1568901346375-23c9450c58cd?w=400&q=80"),
    ("Pasta", "fa-solid fa-bowl-food", f"{U}photo-1621996346565-e3dbc646d9a9?w=400&q=80"),
    ("Chinese", "fa-solid fa-bowl-rice", f"{U}photo-1585032226651-759b368d7246?w=400&q=80"),
    ("South Indian", "fa-solid fa-drumstick-bite", f"{U}photo-1630383249896-424e482df921?w=400&q=80"),
    ("Desserts", "fa-solid fa-ice-cream", f"{U}photo-1551024506-0bccd828d307?w=400&q=80"),
    ("Drinks", "fa-solid fa-mug-hot", f"{U}photo-1544145945-f90425340c7e?w=400&q=80"),
]

ITEMS = [
    ("Margherita Pizza", "Pizza", 299, "Wood-fired base, San Marzano tomatoes, fresh basil and mozzarella.", f"{U}photo-1574071318508-1cdbab80d002?w=800&q=80", True),
    ("Farmhouse Pizza", "Pizza", 379, "Loaded with capsicum, onion, corn, mushroom and extra cheese.", f"{U}photo-1565299624946-b28f40a0ae38?w=800&q=80", True),
    ("Classic Cheese Burger", "Burger", 219, "Juicy grilled patty, cheddar, lettuce and house burger sauce.", f"{U}photo-1568901346375-23c9450c58cd?w=800&q=80", True),
    ("Peri Peri Chicken Burger", "Burger", 279, "Crispy chicken fillet tossed in fiery peri peri seasoning.", f"{U}photo-1550547660-d9450f859349?w=800&q=80", False),
    ("Alfredo Pasta", "Pasta", 329, "Creamy parmesan alfredo with herbs and cracked pepper.", f"{U}photo-1621996346565-e3dbc646d9a9?w=800&q=80", True),
    ("Arrabbiata Penne", "Pasta", 299, "Spicy tomato garlic sauce with chilli flakes and olives.", f"{U}photo-1608219992759-8d74ed8d76eb?w=800&q=80", False),
    ("Hakka Noodles", "Chinese", 249, "Wok-tossed noodles with crunchy vegetables and soy.", f"{U}photo-1585032226651-759b368d7246?w=800&q=80", True),
    ("Chilli Paneer", "Chinese", 289, "Crispy paneer cubes in a sweet and spicy chilli glaze.", f"{U}photo-1626074353765-517a681e40be?w=800&q=80", False),
    ("Masala Dosa", "South Indian", 179, "Crisp rice crepe with spiced potato masala, sambar & chutney.", f"{U}photo-1630383249896-424e482df921?w=800&q=80", True),
    ("Idli Sambar", "South Indian", 129, "Steamed rice cakes served with hot sambar and coconut chutney.", f"{U}photo-1589301760014-d929f3979dbc?w=800&q=80", False),
    ("Molten Choco Lava", "Desserts", 189, "Warm chocolate cake with a gooey molten centre.", f"{U}photo-1624353365286-3f8d62daad51?w=800&q=80", True),
    ("Classic Tiramisu", "Desserts", 249, "Espresso-soaked ladyfingers layered with mascarpone cream.", f"{U}photo-1571877227200-a0d98ea607e9?w=800&q=80", False),
    ("Masala Chai", "Drinks", 79, "Slow-brewed tea with ginger, cardamom and fresh milk.", f"{U}photo-1571934811356-5cc061b6821f?w=800&q=80", False),
    ("Fresh Lime Soda", "Drinks", 99, "Chilled soda with lime, mint and a pinch of black salt.", f"{U}photo-1544145945-f90425340c7e?w=800&q=80", True),
]

GALLERY = [
    ("Chef's special platter", f"{U}photo-1504674900247-0877df9cc836?w=800&q=80"),
    ("Our dining hall", f"{U}photo-1517248135467-4c7edcad34c4?w=800&q=80"),
    ("Wood-fired oven", f"{U}photo-1590947132387-155cc02f3212?w=800&q=80"),
    ("Fresh ingredients", f"{U}photo-1466637574441-749b8f19452f?w=800&q=80"),
    ("Evening ambience", f"{U}photo-1552566626-52f8b828add9?w=800&q=80"),
    ("Dessert counter", f"{U}photo-1551024506-0bccd828d307?w=800&q=80"),
]

TESTIMONIALS = [
    ("Ananya Shah", "Food blogger", "The butter-soft paneer and the wood-fired pizza are worth the drive. Service was warm and fast."),
    ("Rahul Mehta", "Regular guest", "We celebrate every family birthday here. The staff remembers our table and our order!"),
    ("Priya Nair", "Guest", "Cleanest kitchen, freshest South Indian breakfast in the city. The filter coffee is perfect."),
]

CUSTOMERS = [
    ("Nita Kachhadiya", "9825012345", "nita@example.com", "22 Satellite Road, Ahmedabad"),
    ("Arjun Patel", "9825067890", "arjun@example.com", "8 CG Road, Ahmedabad"),
    ("Sneha Desai", "9898011223", "sneha@example.com", "14 Vastrapur, Ahmedabad"),
    ("Vikram Rao", "9723344556", "vikram@example.com", "5 Bopal, Ahmedabad"),
    ("Meera Joshi", "9601122334", "meera@example.com", "31 Prahladnagar, Ahmedabad"),
]


class Command(BaseCommand):
    help = "Seed the database with demo restaurant data"

    def handle(self, *args, **options):
        RestaurantSetting.load()

        admin = self._user("admin", "Admin@12345", "Restaurant Admin", Profile.ADMIN, superuser=True)
        self._user("chef", "Chef@12345", "Head Chef", Profile.CHEF)

        for name, icon, image in CATEGORIES:
            Category.objects.get_or_create(name=name, defaults={"icon": icon, "image_url": image})
        categories = {c.name: c for c in Category.objects.all()}

        for name, category, price, description, image, popular in ITEMS:
            MenuItem.objects.get_or_create(
                name=name,
                defaults={
                    "category": categories[category],
                    "price": Decimal(price),
                    "description": description,
                    "image_url": image,
                    "is_popular": popular,
                    "is_available": True,
                },
            )
        items = list(MenuItem.objects.all())

        for title, url in GALLERY:
            GalleryImage.objects.get_or_create(title=title, defaults={"image_url": url})
        for name, role, message in TESTIMONIALS:
            Testimonial.objects.get_or_create(
                name=name,
                defaults={
                    "role": role,
                    "message": message,
                    "avatar_url": f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=FC8019&color=fff",
                },
            )

        for number in range(1, 13):
            RestaurantTable.objects.get_or_create(
                number=number, defaults={"capacity": random.choice([2, 4, 4, 6, 8])}
            )
        tables = list(RestaurantTable.objects.all())

        customers = []
        for name, mobile, email, address in CUSTOMERS:
            customer, _ = Customer.objects.get_or_create(
                mobile=mobile, defaults={"name": name, "email": email, "address": address}
            )
            customers.append(customer)

        # A demo customer login wired to the first customer record
        demo_user = self._user("guest", "Guest@12345", "Nita Kachhadiya", Profile.CUSTOMER)
        if customers[0].user is None:
            customers[0].user = demo_user
            customers[0].save()

        today = timezone.localdate()
        if not Reservation.objects.exists():
            for offset in range(-3, 5):
                Reservation.objects.create(
                    customer=random.choice(customers),
                    table=random.choice(tables),
                    date=today + timedelta(days=offset),
                    time=random.choice(["12:30", "13:00", "19:30", "20:45"]),
                    guests=random.randint(2, 6),
                    status=Reservation.COMPLETED if offset < 0 else Reservation.RESERVED,
                )

        # Reflect upcoming reservations on the table board
        for reservation in Reservation.objects.filter(status=Reservation.RESERVED, date__gte=today):
            RestaurantTable.objects.filter(pk=reservation.table_id).update(status=RestaurantTable.RESERVED)
        for table in random.sample(tables, 2):
            RestaurantTable.objects.filter(pk=table.pk).update(status=RestaurantTable.OCCUPIED)

        if not Order.objects.exists():
            for day_offset in range(0, 90, 6):
                order = Order.objects.create(
                    customer=random.choice(customers),
                    table=random.choice(tables),
                    status=random.choice([s for s, _ in Order.STATUS_CHOICES]),
                    created_at=timezone.now() - timedelta(days=day_offset, hours=random.randint(0, 8)),
                )
                for item in random.sample(items, random.randint(1, 4)):
                    OrderItem.objects.create(order=order, item=item, quantity=random.randint(1, 3))

        if not Bill.objects.exists():
            for order in Order.objects.all():
                bill = Bill.objects.create(
                    customer=order.customer,
                    order=order,
                    payment_method=random.choice([Bill.CASH, Bill.CARD, Bill.UPI]),
                    payment_status=random.choice([Bill.PAID, Bill.PAID, Bill.UNPAID]),
                    created_at=order.created_at,
                )
                for line in order.items.all():
                    BillItem.objects.create(
                        bill=bill, item=line.item, quantity=line.quantity, price=line.item.price
                    )

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        self.stdout.write("  admin / Admin@12345   (custom admin dashboard)")
        self.stdout.write("  chef  / Chef@12345    (kitchen access)")
        self.stdout.write("  guest / Guest@12345   (customer account)")
        self.stdout.write(f"  superuser email: {admin.email or 'not set'}")

    def _user(self, username, password, full_name, role, superuser=False):
        user, created = User.objects.get_or_create(
            username=username, defaults={"first_name": full_name, "email": f"{username}@example.com"}
        )
        if created:
            user.set_password(password)
        user.is_staff = superuser
        user.is_superuser = superuser
        user.save()
        Profile.objects.update_or_create(user=user, defaults={"role": role})
        return user
