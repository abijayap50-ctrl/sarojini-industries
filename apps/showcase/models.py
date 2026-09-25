from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class WorkshopProfile(models.Model):
    name = models.CharField(max_length=200, default="Sarojini Steel Works")
    tagline = models.CharField(max_length=300, default="Precision Architectural Steel & Heavy Fabrication")
    master_welder = models.CharField(max_length=150, default="Er. Vikram Rao (Certified Welding Specialist)")
    phone = models.CharField(max_length=50, default="+91 98450 12345")
    whatsapp_number = models.CharField(max_length=30, default="919845012345", help_text="Number with country code, no + or spaces")
    email = models.EmailField(default="contact@sarojinisteel.com")
    workshop_address = models.CharField(max_length=300, default="Plot 42, Heavy Industrial Fabrications Yard, Phase 2")
    city = models.CharField(max_length=100, default="Hyderabad, Telangana")
    working_hours = models.CharField(max_length=150, default="Mon - Sat: 8:00 AM - 7:30 PM (Sunday Site Visits on Request)")
    years_experience = models.PositiveIntegerField(default=15)
    projects_completed = models.PositiveIntegerField(default=650)
    warranty_years = models.PositiveIntegerField(default=10)
    certification_badge = models.CharField(max_length=200, default="AWS D1.1 Structural Welding & IS 2062 Grade Steel")
    google_maps_url = models.URLField(max_length=500, blank=True, default="https://maps.google.com")

    class Meta:
        verbose_name = "Workshop Profile & Contact Settings"
        verbose_name_plural = "Workshop Profile & Contact Settings"

    def __str__(self):
        return self.name

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class WorkCategory(models.Model):
    name = models.CharField(max_length=150, unique=True, help_text="e.g. Gates & Entrances, Steel Roofs, Car Parking")
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    badge_text = models.CharField(max_length=100, default="Heavy Duty Fabrication", help_text="e.g. Heavy Duty, Laser Cut, Pre-Fab")
    icon_svg = models.TextField(blank=True, help_text="Custom SVG icon code or icon keyword")
    short_description = models.TextField(help_text="Brief summary shown on category headers and cards")
    display_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first in navbar and page")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this section from the public website")

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Work Category / Section"
        verbose_name_plural = "Work Categories / Sections"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('showcase:category_detail', kwargs={'slug': self.slug})

    @property
    def active_projects(self):
        return self.projects.filter(is_active=True).order_by('display_order', '-created_at')


class ProjectShowcase(models.Model):
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=220, help_text="e.g. 14ft Modern Sliding Gate with Laser Cut Panel")
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    subtitle = models.CharField(max_length=260, blank=True, help_text="e.g. Heavy cantilever sliding gate with Italian automated motor track")
    description = models.TextField(help_text="Detailed engineering and fabrication notes")
    cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    cover_image_url = models.CharField(max_length=500, blank=True, help_text="Direct static or external fallback image URL")

    # Technical Specifications
    steel_grade = models.CharField(max_length=150, default="IS 2062 Grade Mild Steel", help_text="e.g. IS 2062 Structural Mild Steel / Tata Tiscon")
    dimensions = models.CharField(max_length=150, default="Custom Dimensions Available", help_text="e.g. 14ft × 7ft Height (Customizable)")
    thickness_gauge = models.CharField(max_length=150, default="2.0mm Heavy Tube Gauge", help_text="e.g. 2.0mm / 2.5mm MS Square Tube")
    coating_finish = models.CharField(max_length=150, default="Anti-Rust Zinc Primer + 2 Coats PU Enamel", help_text="e.g. Zinc Epoxy Primer + Matte Finish")
    weld_standard = models.CharField(max_length=150, default="AWS D1.1 Certified Welds", help_text="e.g. Full-penetration structural MIG weld")
    estimated_timeline = models.CharField(max_length=100, default="4 - 7 Working Days", help_text="e.g. 3-5 Days Fabrication + 1 Day Installation")
    site_location = models.CharField(max_length=150, default="Hyderabad & Surrounding Regions", help_text="e.g. Jubilee Hills, Hyderabad")

    # Metrics & Highlights
    rating_score = models.DecimalField(max_digits=2, decimal_places=1, default=4.9)
    review_count = models.PositiveIntegerField(default=84)
    is_featured = models.BooleanField(default=True, help_text="Feature this card prominently on homepage")
    is_active = models.BooleanField(default=True, help_text="Visible to public")
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Project Showcase Item"
        verbose_name_plural = "Project Showcase Items"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    def get_absolute_url(self):
        return reverse('showcase:project_detail', kwargs={'slug': self.slug})

    @property
    def primary_image(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        return "/static/images/placeholder_welder.jpg"


class ProjectImage(models.Model):
    project = models.ForeignKey(ProjectShowcase, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='projects/gallery/', blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True)
    caption = models.CharField(max_length=200, blank=True, help_text="e.g. Weld seam close-up, installation on site")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Project Gallery Photo"
        verbose_name_plural = "Project Gallery Photos"

    def __str__(self):
        return f"Photo for {self.project.title}"

    @property
    def url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "/static/images/placeholder_welder.jpg"


class ClientInquiry(models.Model):
    STATUS_NEW = 'NEW'
    STATUS_CONTACTED = 'CONTACTED'
    STATUS_SITE_VISIT = 'SITE_VISIT'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CANCELLED = 'CANCELLED'

    STATUS_CHOICES = [
        (STATUS_NEW, '⭐ New Inquiry'),
        (STATUS_CONTACTED, '📞 Contacted / Quoting'),
        (STATUS_SITE_VISIT, '📐 Site Visit Scheduled'),
        (STATUS_COMPLETED, '✅ Deal Closed / Completed'),
        (STATUS_CANCELLED, '❌ Cancelled / Closed'),
    ]

    name = models.CharField(max_length=150, verbose_name="Customer Name")
    phone = models.CharField(max_length=30, verbose_name="Phone Number")
    email = models.EmailField(blank=True, null=True, verbose_name="Email (Optional)")
    service_interested = models.CharField(max_length=150, verbose_name="Item / Service Needed", default="Main Entrance Gate")
    site_location = models.CharField(max_length=200, verbose_name="Site / Project Location", blank=True, help_text="e.g. Banjara Hills, Hyderabad")
    dimensions_or_notes = models.TextField(blank=True, verbose_name="Approximate Dimensions / Requirements")
    attachment = models.FileField(upload_to='inquiries/drawings/', blank=True, null=True, verbose_name="Rough Sketch / Blueprint / Site Photo")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_NEW)
    admin_remarks = models.TextField(blank=True, verbose_name="Internal Welder Notes (Quotations, appointments)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Quote & Measurement Request"
        verbose_name_plural = "Customer Quote & Measurement Requests"

    def __str__(self):
        return f"{self.name} - {self.service_interested} ({self.phone})"
