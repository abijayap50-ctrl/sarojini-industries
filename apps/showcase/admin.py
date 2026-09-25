from django.contrib import admin
from django.utils.html import format_html
from .models import WorkshopProfile, WorkCategory, ProjectShowcase, ProjectImage, ClientInquiry

admin.site.site_header = "Sarojini Steel Works &bull; Fabrication Admin"
admin.site.site_title = "Sarojini Steel Portal"
admin.site.index_title = "Workshop Showcase & Customer Inquiries Control"


@admin.register(WorkshopProfile)
class WorkshopProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'whatsapp_number', 'city', 'projects_completed', 'years_experience')

    def has_add_permission(self, request):
        # Only allow 1 profile row
        return not WorkshopProfile.objects.exists()


class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'display_order', 'image_url')
    verbose_name = "Additional Gallery Photo"
    verbose_name_plural = "Additional Gallery Photos (Upload for Slider & Blueprint)"


@admin.register(ProjectShowcase)
class ProjectShowcaseAdmin(admin.ModelAdmin):
    list_display = ('preview_thumbnail', 'title', 'category_badge', 'steel_grade', 'dimensions', 'rating_score', 'is_featured', 'is_active', 'display_order')
    list_filter = ('category', 'is_featured', 'is_active', 'steel_grade')
    search_fields = ('title', 'description', 'site_location')
    list_editable = ('display_order', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    fieldsets = (
        ("📸 Main Photo & Overview", {
            'fields': ('cover_image', 'category', 'title', 'slug', 'subtitle', 'description', 'cover_image_url'),
            'description': "Tap the camera button to take a photo of the completed steel fabrication with your phone or select from gallery.",
        }),
        ("⚙️ Structural & Technical Specifications", {
            'fields': ('steel_grade', 'dimensions', 'thickness_gauge', 'coating_finish', 'weld_standard', 'estimated_timeline', 'site_location'),
        }),
        ("⭐ Ratings & Visibility Settings", {
            'fields': ('rating_score', 'review_count', 'is_featured', 'is_active', 'display_order'),
        }),
    )

    def category_badge(self, obj):
        return format_html(
            '<span style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); padding: 2px 8px; border-radius: 9999px; font-weight: 700; font-size: 11px;">{}</span>',
            obj.category.name
        )
    category_badge.short_description = "Category"

    def preview_thumbnail(self, obj):
        img_url = obj.primary_image
        return format_html('<img src="{}" style="width: 54px; height: 38px; object-fit: cover; border-radius: 8px; border: 1px solid #475569; box-shadow: 0 2px 6px rgba(0,0,0,0.3);" />', img_url)
    preview_thumbnail.short_description = "Photo"


@admin.register(WorkCategory)
class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'badge_text', 'display_order', 'project_count', 'is_active')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'badge_text', 'short_description')

    def project_count(self, obj):
        count = obj.projects.count()
        return format_html('<b>{} projects</b>', count)
    project_count.short_description = "Showcase Count"


@admin.register(ClientInquiry)
class ClientInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service_interested', 'site_location', 'status_badge', 'created_at')
    list_filter = ('status', 'service_interested', 'created_at')
    search_fields = ('name', 'phone', 'site_location', 'dimensions_or_notes')
    list_editable = ()
    readonly_fields = ('created_at',)
    fieldsets = (
        ("Customer Details", {
            'fields': ('name', 'phone', 'email', 'service_interested', 'site_location')
        }),
        ("Inquiry Details", {
            'fields': ('dimensions_or_notes', 'attachment', 'created_at')
        }),
        ("Welder Status & Remarks", {
            'fields': ('status', 'admin_remarks')
        }),
    )

    def status_badge(self, obj):
        colors = {
            ClientInquiry.STATUS_NEW: '#f59e0b',
            ClientInquiry.STATUS_CONTACTED: '#38bdf8',
            ClientInquiry.STATUS_SITE_VISIT: '#a855f7',
            ClientInquiry.STATUS_COMPLETED: '#10b981',
            ClientInquiry.STATUS_CANCELLED: '#ef4444',
        }
        color = colors.get(obj.status, '#94a3b8')
        return format_html(
            '<span style="background: {}; color: #020617; font-weight: bold; font-size: 11px; padding: 3px 8px; border-radius: 9999px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
