from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import staff_required
from core.models import RestaurantSetting

from .forms import BillForm, BillItemFormSet
from .models import Bill
from .utils import build_pdf


@staff_required
def bill_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    bills = Bill.objects.select_related("customer")
    if query:
        bills = bills.filter(Q(invoice_number__icontains=query) | Q(customer__name__icontains=query))
    if status:
        bills = bills.filter(payment_status=status)
    page = Paginator(bills, 10).get_page(request.GET.get("page"))
    return render(request, "billing/list.html", {"page_obj": page, "query": query, "status": status})


@staff_required
def bill_add(request):
    form = BillForm(request.POST or None, initial={"gst_percent": RestaurantSetting.load().gst_percent})
    formset = BillItemFormSet(request.POST or None)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        bill = form.save()
        formset.instance = bill
        formset.save()
        messages.success(request, f"Bill {bill.invoice_number} generated.")
        return redirect("billing:detail", pk=bill.pk)
    return render(request, "billing/form.html", {"form": form, "formset": formset, "title": "Generate Bill"})


@staff_required
def bill_edit(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    form = BillForm(request.POST or None, instance=bill)
    formset = BillItemFormSet(request.POST or None, instance=bill)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, "Bill updated.")
        return redirect("billing:detail", pk=bill.pk)
    return render(request, "billing/form.html", {"form": form, "formset": formset, "title": "Update Bill"})


@staff_required
def bill_delete(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == "POST":
        bill.delete()
        messages.success(request, "Bill deleted.")
        return redirect("billing:list")
    return render(request, "confirm_delete.html", {"object": bill, "back_url": "billing:list"})


@staff_required
def bill_detail(request, pk):
    """Printable invoice page."""
    bill = get_object_or_404(Bill.objects.prefetch_related("items__item"), pk=pk)
    return render(request, "billing/invoice.html", {"bill": bill})


@staff_required
def bill_pdf(request, pk):
    bill = get_object_or_404(Bill.objects.prefetch_related("items__item"), pk=pk)
    site = RestaurantSetting.load()
    rows = [["Item", "Qty", "Price", "Subtotal"]]
    for line in bill.items.all():
        rows.append([line.item.name, str(line.quantity), f"{line.price:.2f}", f"{line.subtotal:.2f}"])
    rows += [
        ["", "", "Subtotal", f"{bill.subtotal:.2f}"],
        ["", "", f"GST ({bill.gst_percent}%)", f"{bill.gst_amount:.2f}"],
        ["", "", "Grand Total", f"{bill.grand_total:.2f}"],
    ]
    header = [
        f"<b>{site.name}</b> &nbsp;|&nbsp; {site.address}",
        f"Invoice: <b>{bill.invoice_number}</b> &nbsp;|&nbsp; Date: {bill.created_at:%d %b %Y %H:%M}",
        f"Customer: {bill.customer.name} ({bill.customer.mobile})",
        f"Payment: {bill.get_payment_method_display()} - {bill.get_payment_status_display()}",
    ]
    return build_pdf(
        "TAX INVOICE", header, rows, f"{bill.invoice_number}.pdf", footer="Thank you for dining with us!"
    )


@staff_required
def bill_mark_paid(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    bill.payment_status = Bill.PAID
    bill.save()
    messages.success(request, f"{bill.invoice_number} marked as paid.")
    return redirect("billing:list")
