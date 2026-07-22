from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from directory.sitemaps import CategorySitemap, GuideSitemap, StaticSitemap, ToolSitemap

sitemaps = {
    "static": StaticSitemap,
    "categories": CategorySitemap,
    "tools": ToolSitemap,
    "guides": GuideSitemap,
}

urlpatterns = [
    path("harit-admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("", include("directory.urls")),
]