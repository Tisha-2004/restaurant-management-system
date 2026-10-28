from .models import RestaurantSetting


def site_settings(request):
    """Make restaurant branding available in every template as `site`."""
    return {"site": RestaurantSetting.load()}
