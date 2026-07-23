from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

from directory.sitemaps import (
    CategorySitemap, CitySitemap, GuideSitemap, StaticSitemap, ToolSitemap,
)

sitemaps = {
    "static": StaticSitemap,
    "categories": CategorySitemap,
    "tools": ToolSitemap,
    "guides": GuideSitemap,
    "cities": CitySitemap,
}

urlpatterns = [
    path("harit-admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("llms.txt", TemplateView.as_view(template_name="llms.txt", content_type="text/plain")),
    path("site.webmanifest", TemplateView.as_view(template_name="site.webmanifest", content_type="application/manifest+json")),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("img/favicon.ico"), permanent=True)),
    path("", include("directory.urls")),
]
handler404 = "directory.views.custom_404"
