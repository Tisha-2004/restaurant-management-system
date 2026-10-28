from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required

from .forms import OrderForm, OrderItemFormSet
from .models import Order


@staff_required
def kitchen_dashboard(request):
    """Chef view: orders grouped by status with quick status buttons."""
    query = request.GET.get("q", "").strip()
    orders = Order.objects.select_related("customer", "table").prefetch_related("items__item")
    if query:
        orders = orders.filter(Q(number__icontains=query) | Q(customer__name__icontains=query))
    columns = [
        (label, [o for o in orders if o.status == value]) for value, label in Order.STATUS_CHOICES
    ]
    return render(request, "kitchen/dashboard.html", {"columns": columns, "query": query})


@staff_required
def order_list(request):
    orders = Order.objects.select_related("customer", "table")
    status = request.GET.get("status", "")
    if status:
        orders = orders.filter(status=status)
    page = Paginator(orders, 10).get_page(request.GET.get("page"))
    return render(
        request, "kitchen/list.html", {"page_obj": page, "status": status, "statuses": Order.STATUS_CHOICES}
    )


@staff_required
def order_add(request):
    form = OrderForm(request.POST or None)
    formset = OrderItemFormSet(request.POST or None)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        order = form.save()
        formset.instance = order
        formset.save()
        messages.success(request, f"Order {order.number} created.")
        return redirect("kitchen:dashboard")
    return render(request, "kitchen/form.html", {"form": form, "formset": formset, "title": "New Order"})


@staff_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=order)
    formset = OrderItemFormSet(request.POST or None, instance=order)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, "Order updated.")
        return redirect("kitchen:dashboard")
    return render(request, "kitchen/form.html", {"form": form, "formset": formset, "title": "Update Order"})


@staff_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted.")
        return redirect("kitchen:list")
    return render(request, "confirm_delete.html", {"object": order, "back_url": "kitchen:list"})


@staff_required
def order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)
    valid = dict(Order.STATUS_CHOICES)
    if status in valid:
        order.status = status
        order.save()
        messages.success(request, f"{order.number} marked {valid[status]}.")
    else:
        messages.error(request, "Unknown order status.")
    return redirect(request.GET.get("next") or "kitchen:dashboard")


@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related("items__item"), pk=pk)
    return render(request, "kitchen/detail.html", {"order": order})
