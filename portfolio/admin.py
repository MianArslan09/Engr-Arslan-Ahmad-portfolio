from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Experience, Certification, ContactMessage

# Main branding
admin.site.site_header = "Arslan Ahmad Portfolio Admin"
admin.site.site_title = "Portfolio Control Panel"
admin.site.index_title = "Welcome back, Arslan"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "order", "preview_image", "created_at")
    list_editable = ("is_featured", "order")
    list_filter = ("category", "is_featured")
    search_fields = ("title", "tagline", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "preview_image")
    fieldsets = (
        ("Core Info", {"fields": ("title", "slug", "category", "tagline", "description")}),
        ("Tech & Links", {"fields": ("tech_stack", "github_url", "live_url")}),
        ("Image (use URL or upload, not both)", {"fields": ("image_url", "image", "preview_image")}),
        ("Display", {"fields": ("is_featured", "order", "created_at")}),
    )

    def preview_image(self, obj):
        src = obj.get_image()
        if src:
            return format_html('<img src="{}" style="height:50px;border-radius:6px;object-fit:cover;" />', src)
        return "-"
    preview_image.short_description = "Preview"

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "experience_type", "start_date", "is_current", "order")
    list_editable = ("order", "is_current")
    list_filter = ("experience_type", "is_current")
    search_fields = ("company", "role", "tech_used")
    fieldsets = (
        ("Role Details", {"fields": ("company", "role", "experience_type", "location")}),
        ("Timeline", {"fields": ("start_date", "end_date", "is_current")}),
        ("Details", {"fields": ("responsibilities", "tech_used", "order")}),
    )

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issue_date", "badge_icon", "order")
    list_editable = ("order",)
    list_filter = ("issuer",)
    search_fields = ("title", "description")
    fieldsets = (
        ("Certificate", {"fields": ("title", "issuer", "issuer_display", "badge_icon")}),
        ("Details", {"fields": ("description", "credential_url", "issue_date", "order")}),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "status", "submitted_at", "ip_address")
    list_editable = ("status",)
    list_filter = ("status", "submitted_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "submitted_at", "ip_address")

    def has_add_permission(self, request):
        return False  # Contact messages are inbound only; no manual creation