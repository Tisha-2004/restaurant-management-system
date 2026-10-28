from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import staff_required
from .forms import RegisterForm, StyledLoginForm, UserForm
from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome aboard! Your account has been created.")
        return redirect("accounts:my_dashboard")
    return render(request, "register.html", {"form": form})


def login_view(request):
    """Customer login page."""
    if request.user.is_authenticated:
        return redirect("accounts:my_dashboard")
    form = StyledLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f"Welcome back, {form.get_user().first_name or form.get_user().username}!")
        return redirect("accounts:my_dashboard")
    return render(request, "login.html", {"form": form})


def admin_login_view(request):
    """Separate staff login that only accepts staff/chef/admin accounts."""
    form = StyledLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        profile = getattr(user, "profile", None)
        if user.is_superuser or (profile and profile.is_staff_member):
            login(request, user)
            messages.success(request, "Signed in to the admin dashboard.")
            return redirect("dashboard:home")
        messages.error(request, "This account is not a staff account.")
    return render(request, "admin_login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("core:home")


@login_required
def my_dashboard(request):
    """Customer-facing dashboard: their reservations, orders and bills."""
    customer = getattr(request.user, "customer", None)
    context = {
        "customer": customer,
        "reservations": customer.reservations.select_related("table")[:10] if customer else [],
        "orders": customer.orders.prefetch_related("items__item")[:10] if customer else [],
        "bills": customer.bills.all()[:10] if customer else [],
    }
    return render(request, "accounts/my_dashboard.html", context)


@staff_required
def user_list(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.select_related("profile").order_by("username")
    if query:
        users = users.filter(username__icontains=query)
    return render(request, "accounts/user_list.html", {"users": users, "query": query})


@staff_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, _ = Profile.objects.get_or_create(user=user)
    form = UserForm(request.POST or None, instance=user, initial={"role": profile.role})
    if request.method == "POST" and form.is_valid():
        form.save()
        profile.role = form.cleaned_data["role"]
        profile.save()
        messages.success(request, "User updated successfully.")
        return redirect("accounts:user_list")
    return render(request, "accounts/user_form.html", {"form": form, "object": user})


@staff_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted.")
        return redirect("accounts:user_list")
    return render(request, "confirm_delete.html", {"object": user, "back_url": "accounts:user_list"})
