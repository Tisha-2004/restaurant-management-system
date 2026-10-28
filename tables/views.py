from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required

from .forms import TableForm
from .models import RestaurantTable


@staff_required
def table_list(request):
    status = request.GET.get("status", "")
    tables = RestaurantTable.objects.all()
    if status:
        tables = tables.filter(status=status)
    context = {
        "tables": tables,
        "status": status,
        "counts": {
            "available": RestaurantTable.objects.filter(status=RestaurantTable.AVAILABLE).count(),
            "reserved": RestaurantTable.objects.filter(status=RestaurantTable.RESERVED).count(),
            "occupied": RestaurantTable.objects.filter(status=RestaurantTable.OCCUPIED).count(),
        },
    }
    return render(request, "tables/list.html", context)


@staff_required
def table_add(request):
    form = TableForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Table added successfully.")
        return redirect("tables:list")
    return render(request, "tables/form.html", {"form": form, "title": "Add Table"})


@staff_required
def table_edit(request, pk):
    table = get_object_or_404(RestaurantTable, pk=pk)
    form = TableForm(request.POST or None, instance=table)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Table updated successfully.")
        return redirect("tables:list")
    return render(request, "tables/form.html", {"form": form, "title": "Update Table"})


@staff_required
def table_delete(request, pk):
    table = get_object_or_404(RestaurantTable, pk=pk)
    if request.method == "POST":
        table.delete()
        messages.success(request, "Table deleted.")
        return redirect("tables:list")
    return render(request, "confirm_delete.html", {"object": table, "back_url": "tables:list"})


@staff_required
def table_status(request, pk, status):
    """Quick status switch from the colour-coded table grid."""
    table = get_object_or_404(RestaurantTable, pk=pk)
    valid = dict(RestaurantTable.STATUS_CHOICES)
    if status in valid:
        table.status = status
        table.save()
        messages.success(request, f"Table {table.number} marked {valid[status]}.")
    else:
        messages.error(request, "Unknown table status.")
    return redirect("tables:list")
