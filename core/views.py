from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render

from billing.models import Bill
from customers.models import Customer
from kitchen.models import Order
from menu.models import Category, MenuItem
from reservations.models import Reservation

from .forms import ContactForm
from .models import GalleryImage, Testimonial


def home(request):
    context = {
        "categories": Category.objects.all(),
        "popular": MenuItem.objects.filter(is_popular=True, is_available=True).select_related("category")[:8],
        "gallery": GalleryImage.objects.all()[:6],
        "testimonials": Testimonial.objects.filter(is_active=True)[:6],
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html", {"gallery": GalleryImage.objects.all()[:8]})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks for reaching out! We will reply shortly.")
        return redirect("core:contact")
    return render(request, "contact.html", {"form": form})


def gallery(request):
    return render(request, "gallery.html", {"gallery": GalleryImage.objects.all()})


def global_search(request):
    """Global search across customers, food, reservations, orders and bills."""
    query = request.GET.get("q", "").strip()
    results = {"customers": [], "foods": [], "reservations": [], "orders": [], "bills": []}
    if query:
        results["foods"] = MenuItem.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )[:10]
        if request.user.is_authenticated:
            results["customers"] = Customer.objects.filter(
                Q(name__icontains=query) | Q(mobile__icontains=query) | Q(email__icontains=query)
            )[:10]
            results["reservations"] = Reservation.objects.filter(
                Q(customer__name__icontains=query) | Q(table__number__icontains=query)
            )[:10]
            results["orders"] = Order.objects.filter(
                Q(number__icontains=query) | Q(customer__name__icontains=query)
            )[:10]
            results["bills"] = Bill.objects.filter(
                Q(invoice_number__icontains=query) | Q(customer__name__icontains=query)
            )[:10]
    return render(request, "search.html", {"query": query, "results": results})


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
