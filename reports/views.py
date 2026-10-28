"""Daily / monthly / reservation / sales reports with CSV + PDF export."""
import csv
from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.decorators import staff_required
from billing.models import Bill
from billing.utils import build_pdf
from kitchen.models import Order
from menu.models import MenuItem
from reservations.models import Reservation

REPORT_TYPES = [
    ("daily", "Daily Report"),
    ("monthly", "Monthly Report"),
    ("reservation", "Reservation Report"),
    ("sales", "Sales Report"),
]


def _parse_range(request):
    """Read ?start= and ?end= (defaults: current month to today)."""
    today = timezone.localdate()
    def parse(name, fallback):
        raw = request.GET.get(name)
        if raw:
            try:
                return datetime.strptime(raw, "%Y-%m-%d").date()
            except ValueError:
                pass
        return fallback
    return parse("start", today.replace(day=1)), parse("end", today)


def _build_report(kind, start, end):
    """Return (headers, rows, summary) for the requested report type."""
    if kind == "reservation":
        headers = ["Date", "Time", "Customer", "Table", "Guests", "Status"]
        rows = [
            [str(r.date), r.time.strftime("%H:%M"), r.customer.name, r.table.number, r.guests,
             r.get_status_display()]
            for r in Reservation.objects.filter(date__range=(start, end)).select_related("customer", "table")
        ]
        return headers, rows, {"Total reservations": len(rows)}

    if kind == "sales":
        headers = ["Food Item", "Category", "Quantity Sold", "Revenue"]
        totals = {}
        for bill in Bill.objects.filter(created_at__date__range=(start, end)).prefetch_related("items__item"):
            for line in bill.items.all():
                agg = totals.setdefault(line.item_id, {"qty": 0, "amount": Decimal("0")})
                agg["qty"] += line.quantity
                agg["amount"] += line.subtotal
        items = {i.id: i for i in MenuItem.objects.select_related("category").filter(id__in=totals)}
        rows = [
            [items[i].name, items[i].category.name, agg["qty"], f"{agg['amount']:.2f}"]
            for i, agg in sorted(totals.items(), key=lambda kv: -kv[1]["amount"])
        ]
        revenue = sum((agg["amount"] for agg in totals.values()), Decimal("0"))
        return headers, rows, {"Items sold": sum(a["qty"] for a in totals.values()), "Revenue": f"{revenue:.2f}"}

    if kind == "monthly":
        headers = ["Month", "Bills", "Orders", "Reservations", "Revenue"]
        buckets = {}
        for bill in Bill.objects.filter(created_at__date__range=(start, end)).prefetch_related("items__item"):
            key = bill.created_at.strftime("%Y-%m")
            agg = buckets.setdefault(key, {"bills": 0, "revenue": Decimal("0")})
            agg["bills"] += 1
            agg["revenue"] += bill.grand_total
        rows = []
        for key, agg in sorted(buckets.items()):
            year, month = (int(x) for x in key.split("-"))
            rows.append([
                key,
                agg["bills"],
                Order.objects.filter(created_at__year=year, created_at__month=month).count(),
                Reservation.objects.filter(date__year=year, date__month=month).count(),
                f"{agg['revenue']:.2f}",
            ])
        revenue = sum((a["revenue"] for a in buckets.values()), Decimal("0"))
        return headers, rows, {"Months": len(rows), "Revenue": f"{revenue:.2f}"}

    # daily (default)
    headers = ["Invoice", "Date", "Customer", "Payment", "Status", "Grand Total"]
    bills = Bill.objects.filter(created_at__date__range=(start, end)).select_related(
        "customer"
    ).prefetch_related("items__item")
    rows = [
        [b.invoice_number, f"{b.created_at:%Y-%m-%d %H:%M}", b.customer.name,
         b.get_payment_method_display(), b.get_payment_status_display(), f"{b.grand_total:.2f}"]
        for b in bills
    ]
    revenue = sum((b.grand_total for b in bills), Decimal("0"))
    return headers, rows, {"Bills": len(rows), "Revenue": f"{revenue:.2f}"}


@staff_required
def report_view(request):
    kind = request.GET.get("type", "daily")
    start, end = _parse_range(request)
    headers, rows, summary = _build_report(kind, start, end)
    export = request.GET.get("export")

    if export == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{kind}-report-{start}-{end}.csv"'
        writer = csv.writer(response)
        writer.writerow(headers)
        writer.writerows(rows)
        writer.writerow([])
        for label, value in summary.items():
            writer.writerow([label, value])
        return response

    if export == "pdf":
        title = dict(REPORT_TYPES).get(kind, "Report").upper()
        header_lines = [f"Period: {start} to {end}"] + [f"{k}: <b>{v}</b>" for k, v in summary.items()]
        data = [headers] + [[str(c) for c in row] for row in rows] or [headers]
        return build_pdf(title, header_lines, data, f"{kind}-report-{start}-{end}.pdf")

    context = {
        "kind": kind,
        "types": REPORT_TYPES,
        "start": start,
        "end": end,
        "headers": headers,
        "rows": rows,
        "summary": summary,
    }
    return render(request, "reports/index.html", context)
