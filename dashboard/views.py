import json
from datetime import timedelta
from decimal import Decimal

from django.shortcuts import redirect, render
from django.utils import timezone

from accounts.decorators import staff_required
from billing.models import Bill
from core.forms import SettingsForm
from core.models import RestaurantSetting
from customers.models import Customer
from django.contrib import messages
from kitchen.models import Order
from reservations.models import Reservation
from tables.models import RestaurantTable


def _revenue(bills):
    """Bill totals are computed properties, so sum them in Python."""
    return sum((bill.grand_total for bill in bills), Decimal("0"))


@staff_required
def dashboard_home(request):
    today = timezone.localdate()
    bills_today = Bill.objects.filter(created_at__date=today).prefetch_related("items__item")
    all_bills = Bill.objects.prefetch_related("items__item")

    # Last 6 months of revenue / orders / reservations for the charts
    labels, revenue_series, order_series, reservation_series = [], [], [], []
    cursor = today.replace(day=1)
    months = []
    for _ in range(6):
        months.append(cursor)
        cursor = (cursor - timedelta(days=1)).replace(day=1)
    for month_start in reversed(months):
        labels.append(month_start.strftime("%b %Y"))
        month_bills = [b for b in all_bills if b.created_at.date().replace(day=1) == month_start]
        revenue_series.append(float(_revenue(month_bills)))
        order_series.append(
            Order.objects.filter(created_at__year=month_start.year, created_at__month=month_start.month).count()
        )
        reservation_series.append(
            Reservation.objects.filter(date__year=month_start.year, date__month=month_start.month).count()
        )

    context = {
        "total_customers": Customer.objects.count(),
        "orders_today": Order.objects.filter(created_at__date=today).count(),
        "reservations_today": Reservation.objects.filter(date=today).count(),
        "revenue_today": _revenue(bills_today),
        "revenue_total": _revenue(all_bills),
        "tables_available": RestaurantTable.objects.filter(status=RestaurantTable.AVAILABLE).count(),
        "tables_occupied": RestaurantTable.objects.filter(status=RestaurantTable.OCCUPIED).count(),
        "tables_reserved": RestaurantTable.objects.filter(status=RestaurantTable.RESERVED).count(),
        "recent_orders": Order.objects.select_related("customer", "table")[:8],
        "recent_reservations": Reservation.objects.select_related("customer", "table")[:8],
        "chart_labels": json.dumps(labels),
        "chart_revenue": json.dumps(revenue_series),
        "chart_orders": json.dumps(order_series),
        "chart_reservations": json.dumps(reservation_series),
    }
    return render(request, "dashboard/index.html", context)


@staff_required
def settings_view(request):
    site = RestaurantSetting.load()
    form = SettingsForm(request.POST or None, request.FILES or None, instance=site)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Restaurant settings saved.")
        return redirect("dashboard:settings")
    return render(request, "dashboard/settings.html", {"form": form})
