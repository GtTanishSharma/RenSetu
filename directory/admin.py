from django.contrib import admin

from .models import (
    Category, Dealer, Enquiry, Guide, SiteSetting, SupplierApplication, Tool,
)

admin.site.site_header = "HARIT Admin"
admin.site.site_title = "HARIT Admin"
admin.site.index_title = "Manage your green energy directory"


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("region", "owner_whatsapp", "listing_price")

    def has_add_permission(self, request):
        # only one settings row
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "area", "phone", "is_verified", "is_active", "created_at")
    list_editable = ("is_verified", "is_active")
    list_filter = ("is_verified", "is_active", "city", "categories")
    search_fields = ("name", "area", "description")
    filter_horizontal = ("categories",)


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "body")


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "interest", "city", "property_type", "created_at", "is_handled")
    list_editable = ("is_handled",)
    list_filter = ("is_handled", "city", "interest")
    search_fields = ("name", "message")
    readonly_fields = ("created_at",)


@admin.register(SupplierApplication)
class SupplierApplicationAdmin(admin.ModelAdmin):
    list_display = ("business_name", "phone", "city", "services", "created_at", "is_processed")
    list_editable = ("is_processed",)
    list_filter = ("is_processed", "city")
    search_fields = ("business_name", "services", "message")
    readonly_fields = ("created_at",)
