from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category, Guide, Tool


class StaticSitemap(Sitemap):
    protocol = "https"
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "solutions", "dealers", "tools", "learn", "enquiry", "list_business", "about"]

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    protocol = "https"
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("category", args=[obj.slug])


class ToolSitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Tool.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("tool", args=[obj.slug])


class GuideSitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Guide.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("guide", args=[obj.slug])

class CitySitemap(Sitemap):
    protocol = "https"
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        from .views import CITY_SLUGS
        return list(CITY_SLUGS.keys())

    def location(self, item):
        return reverse("city", args=[item])
