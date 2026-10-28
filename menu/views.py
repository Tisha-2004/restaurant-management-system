from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required

from .forms import CategoryForm, MenuItemForm
from .models import Category, MenuItem


def menu_list(request):
    """Public menu with search + category filter."""
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "")
    items = MenuItem.objects.select_related("category")
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_slug:
        items = items.filter(category__slug=category_slug)
    page = Paginator(items, 9).get_page(request.GET.get("page"))
    context = {
        "page_obj": page,
        "categories": Category.objects.all(),
        "query": query,
        "active_category": category_slug,
    }
    return render(request, "menu/list.html", context)


def menu_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    related = MenuItem.objects.filter(category=item.category).exclude(pk=item.pk)[:4]
    return render(request, "menu/detail.html", {"item": item, "related": related})


@staff_required
def menu_manage(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "")
    items = MenuItem.objects.select_related("category")
    if query:
        items = items.filter(name__icontains=query)
    if category_slug:
        items = items.filter(category__slug=category_slug)
    page = Paginator(items, 10).get_page(request.GET.get("page"))
    context = {
        "page_obj": page,
        "categories": Category.objects.all(),
        "query": query,
        "active_category": category_slug,
    }
    return render(request, "menu/manage.html", context)


@staff_required
def menu_add(request):
    form = MenuItemForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Food item added successfully.")
        return redirect("menu:manage")
    return render(request, "menu/form.html", {"form": form, "title": "Add Food Item"})


@staff_required
def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(request.POST or None, request.FILES or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Food item updated successfully.")
        return redirect("menu:manage")
    return render(request, "menu/form.html", {"form": form, "title": "Update Food Item", "object": item})


@staff_required
def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Food item deleted.")
        return redirect("menu:manage")
    return render(request, "confirm_delete.html", {"object": item, "back_url": "menu:manage"})


@staff_required
def category_list(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category created.")
        return redirect("menu:categories")
    return render(request, "menu/categories.html", {"categories": Category.objects.all(), "form": form})


@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted.")
        return redirect("menu:categories")
    return render(request, "confirm_delete.html", {"object": category, "back_url": "menu:categories"})
