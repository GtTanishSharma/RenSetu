from .models import SiteSetting


def site_settings(request):
    """Make site settings (WhatsApp number, region) available in every template."""
    return {"site": SiteSetting.get()}
