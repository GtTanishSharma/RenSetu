from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    FAQ, Category, Dealer, Enquiry, Guide, SiteSetting, SupplierApplication, Tool,
)

admin.site.site_header = "RenSetu Admin"
admin.site.site_title = "RenSetu Admin"
admin.site.index_title = "Manage your green energy directory"


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("region", "owner_whatsapp", "listing_price")

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class DealerResource(resources.ModelResource):
    class Meta:
        model = Dealer
        fields = (
            'id', 'name', 'city', 'area', 'phone', 'whatsapp', 'description',
            'since', 'is_verified', 'is_active', 'address', 'created_at',
        )


@admin.register(Dealer)
class DealerAdmin(ImportExportModelAdmin):
    resource_class = DealerResource
    list_display = ("name", "city", "area", "phone", "is_verified", "is_active", "created_at")
    list_editable = ("is_verified", "is_active")
    list_filter = ("is_verified", "is_active", "city", "categories")
    search_fields = ("name", "area", "description", "phone")
    filter_horizontal = ("categories",)
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "phone", "whatsapp", "address"),
        }),
        ("Location", {
            "fields": ("city", "area"),
        }),
        ("Services & Details", {
            "fields": ("categories", "description", "since"),
        }),
        ("Status", {
            "fields": ("is_verified", "is_active"),
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )


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


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("question", "answer")