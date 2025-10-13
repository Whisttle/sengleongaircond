from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey


# USP Feature Card Model
class USPFeature(Orderable):
    page = ParentalKey('home.HomePage', related_name='usp_features', on_delete=models.CASCADE)
    ICON_CHOICES = [
        ('fas fa-dollar-sign', 'Dollar Sign'),
        ('fas fa-certificate', 'Certificate'),
        ('fas fa-box-open', 'Box Open'),
        ('fas fa-shield-alt', 'Shield'),
        ('fas fa-clipboard-check', 'Clipboard Check'),
        ('fas fa-user-tie', 'User Tie'),
        ('fas fa-headset', 'Headset'),
        ('fas fa-truck', 'Truck')
    ]
    
    icon_class = models.CharField(
        max_length=100,
        choices=ICON_CHOICES,
        default='fas fa-certificate',
        help_text="Select an icon for this feature"
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    
    panels = [
        FieldPanel('icon_class'),
        FieldPanel('title'),
        FieldPanel('description'),
    ]

class PageSection(Orderable):
    page = ParentalKey('home.HomePage', related_name='page_sections', on_delete=models.CASCADE)
    
    SECTION_CHOICES = [
        ('hero', 'Hero Section'),
        ('usp-section', 'USP Features Section'),
        ('expertise-section', 'Statistics/Expertise Section'),
        ('partners', 'Partners Section'),
        ('testimonials', 'Google Reviews Section')
    ]
    
    section_id = models.CharField(
        max_length=50,
        choices=SECTION_CHOICES,
        unique=True,
        help_text="Select which section this represents"
    )
    is_enabled = models.BooleanField(
        default=True,
        help_text="Show/hide this section on the page"
    )
    
    panels = [
        FieldPanel('section_id'),
        FieldPanel('is_enabled'),
    ]
    
    class Meta:
        ordering = ['sort_order']  # This comes from Orderable
        unique_together = ['page', 'section_id']  # Prevent duplicate sections
    
    def __str__(self):
        return f"{self.section_id} ({'Enabled' if self.is_enabled else 'Disabled'})"
    
    def save(self, *args, **kwargs):
        # Auto-populate section_name if not provided
        if not self.section_id:
            self.section_id = dict(self.SECTION_CHOICES).get(self.section_id, self.section_id)
        super().save(*args, **kwargs)



# Statistics Item Model
class StatisticItem(Orderable):
    page = ParentalKey('home.HomePage', related_name='statistics', on_delete=models.CASCADE)
    number = models.CharField(
        max_length=20, 
        help_text="e.g., '3000+', '90%', '4.8+'"
    )
    label = models.CharField(max_length=100)
    
    panels = [
        FieldPanel('number'),
        FieldPanel('label'),
    ]

# class GalleryImage(Orderable):
#     page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='home_images')
#     image = models.ForeignKey(
#         'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
#     )
#     caption = models.CharField(blank=True, max_length=250)
#     panels = [
#         FieldPanel('image'),
#         FieldPanel('caption'),
#     ]

# Brand Partner Model
class BrandPartner(Orderable):
    page = ParentalKey('home.HomePage', related_name='brand_partners', on_delete=models.CASCADE)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    alt_text = models.CharField(max_length=200, help_text="Alt text for the brand image")
    
    panels = [
        FieldPanel('image'),
        FieldPanel('alt_text'),
    ]


# Google Review Model
class GoogleReview(Orderable):
    page = ParentalKey('home.HomePage', related_name='google_reviews', on_delete=models.CASCADE)
    
    AVATAR_COLOR_CHOICES = [
        ('#e91e63', 'Pink'),
        ('#ff5722', 'Deep Orange'),
        ('#795548', 'Brown'),
        ('#607d8b', 'Blue Grey'),
        ('#9c27b0', 'Purple'),
        ('#3f51b5', 'Indigo'),
        ('#2196f3', 'Blue'),
        ('#009688', 'Teal'),
        ('#4caf50', 'Green'),
        ('#ff9800', 'Orange'),
        ('#f44336', 'Red'),
        ('#673ab7', 'Deep Purple'),
    ]
    
    REVIEW_SOURCE_CHOICES = [
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('trustpilot', 'Trustpilot'),
        ('yelp', 'Yelp'),
        ('website', 'Website'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=100,
        help_text="Customer's name"
    )
    profile_picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Optional profile picture - will be cropped to circle"
    )
    avatar_color = models.CharField(
        max_length=7,
        choices=AVATAR_COLOR_CHOICES,
        default='#e91e63',
        help_text="Color for the avatar background (used if no profile picture)"
    )
    
    # Review Content
    review_text = models.TextField(
        max_length=800,
        help_text="The review content - will be truncated with 'Read more' if too long"
    )
    rating = models.IntegerField(
        default=5,
        choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)],
        help_text="Star rating (1-5)"
    )
    
    # Review Source and Date
    review_source = models.CharField(
        max_length=20,
        choices=REVIEW_SOURCE_CHOICES,
        default='google',
        help_text="Platform where the review was posted"
    )
    review_date = models.DateTimeField(
        help_text="Date when the review was posted (leave blank for auto-fill)"
    )
    is_verified = models.BooleanField(
        default=True,
        help_text="Show verified badge"
    )
    
    # Display Options
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this review (will appear first in slider)"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('profile_picture'),
            FieldPanel('avatar_color'),
        ], heading="Reviewer Information"),
        MultiFieldPanel([
            FieldPanel('review_text'),
            FieldPanel('rating'),
            FieldPanel('review_source'),
        ], heading="Review Content"),
        MultiFieldPanel([
            FieldPanel('review_date'),
            FieldPanel('is_verified'),
            FieldPanel('is_featured'),
        ], heading="Review Settings"),
    ]
    
    class Meta:
        ordering = ['-is_featured', '-review_date']
    
    def save(self, *args, **kwargs):
        # Auto-fill review_date if not provided
        if not self.review_date:
            from django.utils import timezone
            self.review_date = timezone.now()
        super().save(*args, **kwargs)
    
    def get_avatar_initial(self):
        """Get the first letter of the name for avatar"""
        return self.name[0].upper() if self.name else '?'
    
    def get_time_ago(self):
        """Get human-readable time since review was posted"""
        from django.utils import timezone
        import datetime
        
        now = timezone.now()
        diff = now - self.review_date
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years != 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            return "Recently"
    
    def get_source_icon(self):
        """Get the appropriate icon class for the review source"""
        icon_map = {
            'google': 'fab fa-google',
            'facebook': 'fab fa-facebook',
            'trustpilot': 'fas fa-star',
            'yelp': 'fab fa-yelp',
            'website': 'fas fa-globe',
        }
        return icon_map.get(self.review_source, 'fas fa-star')
    
    def get_truncated_text(self, max_length=150):
        """Get truncated review text with ellipsis"""
        if len(self.review_text) <= max_length:
            return self.review_text
        return self.review_text[:max_length].rsplit(' ', 1)[0] + '...'
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars ({self.review_source})"


class HomePage(Page):
    # Ensure only one home page can be created
    max_count = 1
    
    # Page Display Options
    show_navigation = models.BooleanField(
        "Show Navigation Bar",
        default=True,
        help_text="Display the navigation header on this page"
    )
    show_footer = models.BooleanField(
        "Show Footer",
        default=True,
        help_text="Display the footer on this page"
    )
    
    # SEO Fields
    meta_description = models.TextField(
        max_length=250,
        blank=True,
        default="Professional air conditioning installation, repair & maintenance in Klang Valley. 20+ years experience, certified technicians, competitive pricing. Call +6012-652 6665 for free quote.",
        help_text="Search engine description (250 characters max)"
    )
    meta_keywords = models.CharField(
        max_length=500,
        blank=True,
        default="air conditioning services Klang Valley, aircond repair KL, aircond installation Selangor, aircon maintenance Malaysia, certified aircond technician, Seng Leong Engineering",
        help_text="Comma-separated keywords for SEO"
    )
    
    # Hero Section
    hero_title = models.CharField(
        max_length=250, 
        default="Your Certified Aircond Supplier in Klang Valley",
        help_text="Main heading displayed in hero section"
    )
    hero_description = RichTextField(
        max_length=800,
        default="We are a certified air conditioning supplier with over 20 years of proven experience. Trusted by residential and commercial clients across Klang Valley area. We offer the lowest pricing without compromising on quality and provide brand-certified systems from all top air conditioner brands. Our solutions guarantee reliability, energy efficiency and long-term value.",
        help_text="Hero section description text",
        features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ]
    )
    hero_background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background image for hero section"
    )
    
    # Form Section
    form_title = models.CharField(
        max_length=100,
        default="Get Free Air Conditioning Quote",
        help_text="Title for the contact form"
    )
    form_subtitle = models.CharField(
        max_length=200,
        default="Contact us today for professional air conditioning supply in Klang Valley",
        help_text="Subtitle for the contact form"
    )
    form_whatsapp_number = models.CharField(
        max_length=20,
        default="60122992909",
        help_text="WhatsApp number (without + sign) for form submissions"
    )
    form_whatsapp_message_template = models.TextField(
        default="Hi! I'm interested in getting a quote for air conditioning service.\n\n*Name:* {name}\n*Email:* {email}\n*Phone:* {phone}\n*Budget:* {budget}\n*Location:* {location}\n*Requirements:* {message}\n\nPlease contact me for a free quote. Thank you!",
        help_text="WhatsApp message template. Use {name}, {email}, {phone}, {budget}, {location}, {message} as placeholders"
    )
    form_success_message = models.CharField(
        max_length=300,
        default="Redirecting to WhatsApp to send your inquiry...",
        help_text="Success message shown before redirecting to WhatsApp"
    )
    
    # Services Section
    services_title = models.CharField(
        max_length=150,
        default="Professional Air Conditioning Supply in Klang Valley",
        help_text="Main title for services section"
    )
    services_subtitle = models.CharField(
        max_length=300,
        default="Certified technicians delivering excellence across Kuala Lumpur, Selangor, and Klang Valley with 20+ years of experience",
        help_text="Subtitle for services section"
    )
    
    # Statistics Section
    stats_title = models.CharField(
        max_length=150,
        default="Our Track Record Speaks for Itself",
        help_text="Title for statistics section"
    )
    stats_subtitle = models.CharField(
        max_length=300,
        default="Numbers that demonstrate our commitment to excellence and customer satisfaction",
        help_text="Subtitle for statistics section"
    )
    
    # Partners Section
    partners_title = models.CharField(
        max_length=150,
        default="Authorized Air Conditioning Brand Partners",
        help_text="Title for partners section"
    )
    partners_subtitle = models.CharField(
        max_length=300,
        default="Official dealer for leading air conditioning brands in Malaysia",
        help_text="Subtitle for partners section"
    )
    
    # Testimonials Section
    testimonials_title = models.CharField(
        max_length=150,
        default="Customer Reviews & Testimonials",
        help_text="Title for testimonials section"
    )
    testimonials_subtitle = models.CharField(
        max_length=300,
        default="Real feedback from satisfied customers across Klang Valley, Selangor, and Kuala Lumpur",
        help_text="Subtitle for testimonials section"
    )
    
    # Google Review Widget Section
    google_widget_enabled = models.BooleanField(
        default=True,
        help_text="Show Google review widget in hero section"
    )
    google_widget_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.7,
        help_text="Overall Google rating (e.g., 4.7)"
    )
    google_widget_review_count = models.PositiveIntegerField(
        default=16892,
        help_text="Total number of Google reviews"
    )
    google_widget_url = models.URLField(
        blank=True,
        default="https://www.google.com/maps/place/Seng+Leong+Engineering+Sdn+Bhd/data=!4m2!3m1!1s0x0:0x8bf3d80f0f4ec0bc?sa=X&ved=1t:2428&ictx=111",
        help_text="Link to Google Business profile/reviews"
    )
    # Contact Section
    company_name = models.CharField(
        max_length=100,
        default="Seng Leong Engineering Sdn Bhd",
        help_text="Company name"
    )
    phone_primary = models.CharField(
        max_length=20,
        default="+6012-652 6665",
        help_text="Primary phone number"
    )
    phone_secondary = models.CharField(
        max_length=20,
        default="+6017-510 6665",
        blank=True,
        help_text="Secondary phone number (optional)"
    )
    address_street = models.CharField(
        max_length=200,
        default="31, Jalan Bendahara 2, Taman Sejati",
        help_text="Street address"
    )
    address_city = models.CharField(
        max_length=50,
        default="Klang",
        help_text="City"
    )
    address_state = models.CharField(
        max_length=50,
        default="Selangor",
        help_text="State"
    )
    address_postcode = models.CharField(
        max_length=10,
        default="41200",
        help_text="Postal code"
    )
    facebook_url = models.URLField(
        blank=True,
        default="https://www.facebook.com/sengleongaircond",
        help_text="Facebook page URL"
    )
    whatsapp_number = models.CharField(
        max_length=20,
        default="60122992909",
        help_text="WhatsApp number (without + sign)"
    )
    whatsapp_message = models.CharField(
        max_length=200,
        default="Hi, I would like to get a quote for air conditioning service",
        help_text="Default WhatsApp message"
    )
    google_maps_embed = models.TextField(
        default='<iframe width="100%" height="300" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?width=100%25&amp;height=600&amp;hl=en&amp;q=31,%20Jalan%20Bendahara%202,%20taman%20sejati,%2041200%20Klang,%20Selangor+(Seng%20Leong%20Engineering%20Sdn%20Bhd)&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"></iframe>',
        help_text="Google Maps embed code"
    )
    
    embed_head_code = models.TextField(
        blank=True,
        help_text="Embed any code in <head> (Google Analytics or Microsoft Clarity)"
    )

    embed_body_code = models.TextField(
        blank=True,
        help_text="Embed any code in <body> (Google Tag manager)"
    )

    # Define content panels with organized tabs
    content_panels = Page.content_panels + [
        InlinePanel('page_sections', heading="Page Structure", 
                   help_text="Sections is structured in order. Uncheck 'is_enabled' to hide sections. Cannot use the same section",
                   min_num=1),
        MultiFieldPanel([
            FieldPanel('show_navigation'),
            FieldPanel('show_footer'),
            FieldPanel('embed_head_code'),
            FieldPanel('embed_body_code'),
        ], heading="Page Display Options"),
    ]
    
    hero_panels = [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_description'),
            FieldPanel('hero_background_image'),
        ], heading="Hero Content"),
        MultiFieldPanel([
            FieldPanel('form_title'),
            FieldPanel('form_subtitle'),
            FieldPanel('form_whatsapp_number'),
            FieldPanel('form_whatsapp_message_template'),
            FieldPanel('form_success_message'),
        ], heading="WhatsApp Contact Form"),
    ]
    
    services_panels = [
        MultiFieldPanel([
            FieldPanel('services_title'),
            FieldPanel('services_subtitle'),
        ], heading="Services Section"),
        InlinePanel('usp_features', heading="USP Features", min_num=1),
    ]
    
    stats_panels = [
        MultiFieldPanel([
            FieldPanel('stats_title'),
            FieldPanel('stats_subtitle'),
        ], heading="Statistics Section"),
        InlinePanel('statistics', heading="Statistics", min_num=1),
    ]
    
    partners_panels = [
        MultiFieldPanel([
            FieldPanel('partners_title'),
            FieldPanel('partners_subtitle'),
            # InlinePanel('home_images', label="Home Images"),
        ], heading="Partners Section"),
        InlinePanel('brand_partners', heading="Brand Partners", min_num=1),
    ]
    
    testimonials_panels = [
        MultiFieldPanel([
            FieldPanel('testimonials_title'),
            FieldPanel('testimonials_subtitle'),
        ], heading="Testimonials Section"),
        MultiFieldPanel([
            FieldPanel('google_widget_enabled'),
            FieldPanel('google_widget_rating'),
            FieldPanel('google_widget_review_count'),
            FieldPanel('google_widget_url'),
        ], heading="Google Review Widget"),
        InlinePanel('google_reviews', heading="Google Reviews", min_num=1),
    ]
    
    contact_panels = [
        MultiFieldPanel([
            FieldPanel('company_name'),
            FieldPanel('phone_primary'),
            FieldPanel('phone_secondary'),
        ], heading="Company Information"),
        MultiFieldPanel([
            FieldPanel('address_street'),
            FieldPanel('address_city'),
            FieldPanel('address_state'),
            FieldPanel('address_postcode'),
        ], heading="Address"),
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('whatsapp_number'),
            FieldPanel('whatsapp_message'),
        ], heading="Social Media"),
        FieldPanel('google_maps_embed'),
    ]
    
    seo_panels = [
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('meta_keywords'),
        ], heading="SEO Meta Tags"),
    ]
    
    # Organize panels into tabs
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General'),
        ObjectList(hero_panels, heading='Hero Section'),
        ObjectList(services_panels, heading='Services'),
        ObjectList(stats_panels, heading='Statistics'),
        ObjectList(partners_panels, heading='Partners'),
        ObjectList(testimonials_panels, heading='Testimonials'),
        ObjectList(contact_panels, heading='Contact'),
        ObjectList(seo_panels, heading='SEO'),
    ])

    def get_ordered_sections(self):
        """Return sections in the order specified by the user"""
        return self.page_sections.filter(is_enabled=True).order_by('sort_order')

    def get_section_dict(self):
        """Return a dictionary mapping section_id to order for use in templates"""
        sections = {}
        for i, section in enumerate(self.get_ordered_sections()):
            sections[section.section_id] = {
                'order': i,
                'enabled': section.is_enabled,
            }
        return sections




