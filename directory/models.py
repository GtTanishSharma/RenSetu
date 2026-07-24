from django.db import models


class SiteSetting(models.Model):
    """Single-row site config the owner edits in admin (WhatsApp number, region)."""
    owner_whatsapp = models.CharField(
        max_length=20, default="919000000000",
        help_text="Country code + number, digits only. e.g. 919812345678",
    )
    region = models.CharField(max_length=80, default="Delhi NCR")
    listing_price = models.CharField(max_length=20, default="₹100")

    class Meta:
        verbose_name = "Site setting"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return f"RenSetu settings ({self.region})"

    @classmethod
    def get(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj


class Category(models.Model):
    slug = models.SlugField(unique=True, help_text="Used in the URL, e.g. 'solar'")
    name = models.CharField(max_length=80)
    short = models.CharField(max_length=160, help_text="One-line tagline on cards")
    icon = models.CharField(
        max_length=20, default="solar",
        help_text="Icon key: solar, heater, wind, rain, ev, battery, biogas, compost, roof, grey",
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower shows first")
    is_active = models.BooleanField(default=True)

    # detail-page content
    intro = models.TextField(blank=True)
    body = models.TextField(blank=True)
    cost = models.CharField(max_length=80, blank=True)
    subsidy = models.CharField(max_length=120, blank=True)
    saving = models.CharField(max_length=80, blank=True)
    payback = models.CharField(max_length=80, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Dealer(models.Model):
    name = models.CharField(max_length=120)
    categories = models.ManyToManyField(Category, related_name="dealers")
    city = models.CharField(max_length=60)
    area = models.CharField(max_length=120)
    address = models.TextField(
        blank=True,
        help_text="Full street address. Shows on dealer profile for credibility.",
    )
    phone = models.CharField(max_length=25)
    whatsapp = models.CharField(
        max_length=20, help_text="Country code + number, digits only",
    )
    description = models.TextField()
    since = models.CharField(max_length=10, blank=True, help_text="Year established, e.g. 2019")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_verified", "name"]

    def __str__(self):
        return self.name


class Tool(models.Model):
    slug = models.SlugField(unique=True, help_text="Fixed keys used by the calculators")
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="tools",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Guide(models.Model):
    slug = models.SlugField(unique=True)
    tag = models.CharField(max_length=40, help_text="Small label, e.g. Subsidy / Basics")
    title = models.CharField(max_length=160)
    body = models.TextField(help_text="Separate paragraphs with a blank line")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.title

    def paragraphs(self):
        return [p.strip() for p in self.body.split("\n\n") if p.strip()]


class Enquiry(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=60, blank=True)
    interest = models.CharField(max_length=120, blank=True)
    property_type = models.CharField(max_length=80, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.interest or 'general'} ({self.created_at:%d %b})"


class SupplierApplication(models.Model):
    business_name = models.CharField(max_length=140)
    contact_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=25)
    city = models.CharField(max_length=60, blank=True)
    services = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.business_name


class FAQ(models.Model):
    """Question/answer pairs shown on category pages and emitted as FAQPage schema.

    These target the long, question-shaped searches that trigger AI answers.
    """
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="faqs",
        null=True, blank=True,
        help_text="Leave blank for a general FAQ shown on the About page.",
    )
    question = models.CharField(max_length=250)
    answer = models.TextField(help_text="Answer directly in the first sentence, then add detail.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["order", "id"]

    def __str__(self):
        return self.question