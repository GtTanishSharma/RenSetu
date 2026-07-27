from pathlib import Path
 
from django.conf import settings # pyright: ignore[reportMissingModuleSource]
from django.contrib import admin # pyright: ignore[reportMissingModuleSource]
from django.contrib.sitemaps.views import sitemap # pyright: ignore[reportMissingModuleSource]
from django.http import FileResponse # pyright: ignore[reportMissingModuleSource]
from django.urls import include, path # pyright: ignore[reportMissingModuleSource]
from django.views.generic import TemplateView # type: ignore
 
from directory.sitemaps import (
    CategorySitemap, CitySitemap, GuideSitemap, StaticSitemap, ToolSitemap,
)
 
BASE_DIR = settings.BASE_DIR
 
sitemaps = {
    "static": StaticSitemap,
    "categories": CategorySitemap,
    "tools": ToolSitemap,
    "guides": GuideSitemap,
    "cities": CitySitemap,
}
 
urlpatterns = [
    path("vatsu-admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("llms.txt", TemplateView.as_view(template_name="llms.txt", content_type="text/plain")),
    path("site.webmanifest", TemplateView.as_view(template_name="site.webmanifest", content_type="application/manifest+json")),
    path("favicon.ico", lambda r: FileResponse(
        open(BASE_DIR / "directory/static/img/favicon.ico", "rb"),
        content_type="image/x-icon")),
    path("", include("directory.urls")),
]
handler404 = "directory.views.custom_404"