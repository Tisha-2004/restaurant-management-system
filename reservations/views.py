import calendar
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import staff_required
from tables.models import RestaurantTable

from .forms import PublicReservationForm, ReservationForm
from .models import Reservation


@staff_required
def reservation_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    reservations = Reservation.objects.select_related("customer", "table")
    if query:
        reservations = reservations.filter(
            Q(customer__name__icontains=query) | Q(customer__mobile__icontains=query)
        )
    if status:
        reservations = reservations.filter(status=status)
    page = Paginator(reservations, 10).get_page(request.GET.get("page"))
    context = {
        "page_obj": page,
        "query": query,
        "status": status,
        "statuses": Reservation.STATUS_CHOICES,
    }
    return render(request, "reservation/list.html", context)


@staff_required
def reservation_add(request):
    form = ReservationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        reservation = form.save()
        _sync_table_status(reservation)
        messages.success(request, "Reservation confirmed.")
        return redirect("reservations:list")
    return render(request, "reservation/form.html", {"form": form, "title": "New Reservation"})


@staff_required
def reservation_edit(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    form = ReservationForm(request.POST or None, instance=reservation)
    if request.method == "POST" and form.is_valid():
        reservation = form.save()
        _sync_table_status(reservation)
        messages.success(request, "Reservation updated.")
        return redirect("reservations:list")
    return render(request, "reservation/form.html", {"form": form, "title": "Update Reservation"})


@staff_required
def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Reservation deleted.")
        return redirect("reservations:list")
    return render(request, "confirm_delete.html", {"object": reservation, "back_url": "reservations:list"})


@login_required
def reservation_cancel(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = Reservation.CANCELLED
    reservation.save()
    if reservation.table.status == RestaurantTable.RESERVED:
        reservation.table.status = RestaurantTable.AVAILABLE
        reservation.table.save()
    messages.success(request, "Reservation cancelled.")
    return redirect(request.GET.get("next") or "reservations:list")


@staff_required
def reservation_calendar(request):
    """Simple month grid showing reservations per day."""
    today = timezone.localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    reservations = Reservation.objects.filter(date__year=year, date__month=month).select_related(
        "customer", "table"
    )
    by_day = {}
    for reservation in reservations:
        by_day.setdefault(reservation.date.day, []).append(reservation)
    weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)
    grid = [[{"day": d, "items": by_day.get(d, [])} for d in week] for week in weeks]
    context = {
        "grid": grid,
        "month_name": date(year, month, 1).strftime("%B %Y"),
        "year": year,
        "month": month,
        "prev": (year - 1, 12) if month == 1 else (year, month - 1),
        "next": (year + 1, 1) if month == 12 else (year, month + 1),
    }
    return render(request, "reservation/calendar.html", context)


@login_required
def book_table(request):
    """Public booking page for logged-in customers."""
    customer = getattr(request.user, "customer", None)
    if customer is None:
        messages.error(request, "Complete your customer profile before booking.")
        return redirect("accounts:my_dashboard")
    form = PublicReservationForm(request.POST or None)
    form.fields["table"].queryset = RestaurantTable.objects.exclude(status=RestaurantTable.OCCUPIED)
    if request.method == "POST" and form.is_valid():
        reservation = form.save(commit=False)
        reservation.customer = customer
        reservation.status = Reservation.RESERVED
        reservation.save()
        _sync_table_status(reservation)
        messages.success(request, "Your table is reserved. See you soon!")
        return redirect("accounts:my_dashboard")
    return render(request, "reservation/book.html", {"form": form})


def _sync_table_status(reservation):
    """Keep the table status in sync with its latest reservation."""
    table = reservation.table
    if reservation.status == Reservation.RESERVED:
        table.status = RestaurantTable.RESERVED
    elif reservation.status in {Reservation.COMPLETED, Reservation.CANCELLED}:
        table.status = RestaurantTable.AVAILABLE
    table.save()
