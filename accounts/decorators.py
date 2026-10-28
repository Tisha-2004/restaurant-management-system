"""Access-control helpers used across the custom admin modules."""
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def staff_required(view):
    """Allow only logged-in staff/chef/admin users (custom dashboard area)."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "Please sign in as staff to continue.")
            return redirect("accounts:admin_login")
        profile = getattr(user, "profile", None)
        if user.is_superuser or (profile and profile.is_staff_member):
            return view(request, *args, **kwargs)
        messages.error(request, "You do not have permission to access the admin area.")
        return redirect("core:home")

    return wrapper
