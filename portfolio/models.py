from django.db import models
from django.utils import timezone

class Project(models.Model):
    CATEGORY_CHOICES = [
        ("ml", "Machine Learning / AI"),
        ("web", "Web Development"),
        ("data", "Data Science / Analytics"),
        ("security", "Cyber Security"),
        ("other", "Other"),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="ml")
    tagline = models.CharField(max_length=300)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500)
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Paste a direct image URL (Unsplash, GitHub raw, Cloudinary)"
    )
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ["order", "-created_at"]

    def __str__(self): 
        return self.title

    def get_tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    def get_image(self):
        if self.image: 
            return self.image.url
        return self.image_url or None


class Experience(models.Model):
    EXPERIENCE_TYPE = [
        ("internship", "Internship"), 
        ("fulltime", "Full-Time"),
        ("parttime", "Part-Time"), 
        ("freelance", "Freelance"),
    ]
    
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE, default="internship")
    location = models.CharField(max_length=200, default="Faisalabad, Pakistan")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    responsibilities = models.TextField(help_text="One bullet per line")
    tech_used = models.CharField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta: 
        ordering = ["order", "-start_date"]

    def __str__(self): 
        return f"{self.role} @ {self.company}"

    def get_responsibilities_list(self):
        return [r.strip() for r in self.responsibilities.splitlines() if r.strip()]

    def get_tech_list(self):
        return [t.strip() for t in self.tech_used.split(",") if t.strip()]

    def get_date_range(self):
        s = self.start_date.strftime("%b %Y")
        if self.is_current: 
            return f"{s} - Present"
        e = self.end_date.strftime("%b %Y") if self.end_date else "Present"
        return f"{s} - {e}"


class Certification(models.Model):
    ISSUER_CHOICES = [
        ("ibm", "IBM / Coursera"), 
        ("google", "Google / Coursera"),
        ("ec_council", "EC-Council"), 
        ("microsoft", "Microsoft"),
        ("other", "Other"),
    ]
    
    title = models.CharField(max_length=300)
    issuer = models.CharField(max_length=30, choices=ISSUER_CHOICES, default="other")
    issuer_display = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    badge_icon = models.CharField(max_length=10, default="trophy")
    order = models.PositiveIntegerField(default=0)

    class Meta: 
        ordering = ["order", "-issue_date"]

    def __str__(self): 
        return f"{self.title} ({self.get_issuer_display()})"

    def get_issuer_name(self):
        return self.issuer_display or self.get_issuer_display()


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ("new", "New"), 
        ("read", "Read"), 
        ("replied", "Replied"),
        ("archived", "Archived"),
    ]
    
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    submitted_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta: 
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"[{self.status.upper()}] {self.name} - {self.subject[:50]}"