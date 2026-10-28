from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required

from .forms import CustomerForm
from .models import Customer


@staff_required
def customer_list(request):
    query = request.GET.get("q", "").strip()
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(
            Q(name__icontains=query) | Q(mobile__icontains=query) | Q(email__icontains=query)
        )
    page = Paginator(customers, 10).get_page(request.GET.get("page"))
    return render(request, "customer/list.html", {"page_obj": page, "query": query})


@staff_required
def customer_add(request):
    form = CustomerForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Customer added successfully.")
        return redirect("customers:list")
    return render(request, "customer/form.html", {"form": form, "title": "Add Customer"})


@staff_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, request.FILES or None, instance=customer)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Customer updated successfully.")
        return redirect("customers:list")
    return render(request, "customer/form.html", {"form": form, "title": "Update Customer"})


@staff_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer deleted.")
        return redirect("customers:list")
    return render(request, "confirm_delete.html", {"object": customer, "back_url": "customers:list"})


@staff_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customer/detail.html", {"customer": customer})
