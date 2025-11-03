from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList, FieldRowPanel
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from .blocks import CallToActionBlock


# Webhook Settings - Editable from Wagtail Admin
@register_setting
class WebhookSettings(BaseSiteSetting):
    """
    Webhook configuration for form submissions
    Accessible in Wagtail Admin under Settings > Webhook Settings
    """
    zapier_webhook_url = models.URLField(
        blank=True,
        default="https://hooks.zapier.com/hooks/catch/530937/ur7g2ql/",
        help_text="Zapier webhook URL to send form submissions to. Leave blank to disable Zapier integration."
    )
    
    webhook_enabled = models.BooleanField(
        default=True,
        help_text="Enable or disable sending data to the webhook"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('webhook_enabled'),
            FieldPanel('zapier_webhook_url'),
        ], heading="Zapier Webhook Configuration"),
    ]
    
    class Meta:
        verbose_name = "Webhook Settings"


# Form Field for HomePage Contact Form
class HomePageFormField(AbstractFormField):
    page = ParentalKey(
        'HomePage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )

 
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


# Thank You Page Settings Model
class ThankYouPageSettings(Orderable):
    page = ParentalKey('home.HomePage', related_name='thank_you_settings', on_delete=models.CASCADE)
    
    # Thank You Container Content
    thank_you_title = models.CharField(
        max_length=100,
        default="Thank You!",
        help_text="Main title displayed on thank you page"
    )
    thank_you_message = models.TextField(
        max_length=500,
        default="Your inquiry has been successfully submitted. We've received your message and will get back to you as soon as possible.",
        help_text="Main thank you message"
    )
    
    # Info Box Content (Rich Text)
    info_box_title = models.CharField(
        max_length=100,
        default="What Happens Next?",
        help_text="Title for the information box"
    )
    info_box_content = RichTextField(
        default="<p>✓ We'll review your inquiry within 24 hours</p><p>✓ Our team will contact you via email or phone</p><p>✓ We'll provide a detailed quote and answer all your questions</p>",
        help_text="Rich text content for the information box",
        features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'code'
        ]
    )
    
    # Button Settings
    home_button_text = models.CharField(
        max_length=50,
        default="Back to Home",
        help_text="Text for the home button"
    )
    submit_another_button_text = models.CharField(
        max_length=50,
        default="Submit Another Inquiry",
        help_text="Text for the submit another inquiry button"
    )
    
    # Contact Section
    contact_section_title = models.CharField(
        max_length=100,
        default="Need Immediate Assistance?",
        help_text="Title for the contact section"
    )
    phone_link_text = models.CharField(
        max_length=50,
        default="Call Us",
        blank=True,
        help_text="Text for the phone link (Phone number us phone primary)"
    )
    whatsapp_link_text = models.CharField(
        max_length=50,
        default="WhatsApp Us",
        blank=True,
        help_text="Text for the WhatsApp link (phone URL uses whatsapp number)"
    )
    
    # Display Options
    show_info_box = models.BooleanField(
        default=True,
        help_text="Show the information box on thank you page"
    )
    show_contact_section = models.BooleanField(
        default=True,
        help_text="Show the contact section on thank you page"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('thank_you_title'),
            FieldPanel('thank_you_message'),
        ], heading="Thank You Content"),
        MultiFieldPanel([
            FieldPanel('show_info_box'),
            FieldPanel('info_box_title'),
            FieldPanel('info_box_content'),
        ], heading="Information Box"),
        MultiFieldPanel([
            FieldPanel('home_button_text'),
            FieldPanel('submit_another_button_text'),
        ], heading="Button Settings"),
        MultiFieldPanel([
            FieldPanel('show_contact_section'),
            FieldPanel('contact_section_title'),
            FieldPanel('phone_link_text'),
            FieldPanel('whatsapp_link_text'),
        ], heading="Contact Section"),
    ]
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Thank You Page Settings"
        verbose_name_plural = "Thank You Page Settings"
    
    def __str__(self):
        return f"Thank You Settings - {self.thank_you_title}"


class HomePage(AbstractEmailForm):
    # Ensure only one home page can be created
    max_count = 1
    
    parent_page_types = [
        'wagtailcore.Page'  # Can only be created under the root page
    ]

    subpage_types = [
        'contact.ContactPage'
    ]
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
    
    # Form Submission Method Toggle
    form_submission_method = models.CharField(
        max_length=20,
        choices=[
            ('whatsapp', 'WhatsApp (JavaScript redirect)'),
            ('email', 'Email (Wagtail form submission)'),
        ],
        default='email',
        help_text="Choose how form submissions should be handled. WhatsApp will redirect users to WhatsApp with pre-filled message. Email will save submissions and send via Mailtrap."
    )
    
    # WhatsApp Settings (only used if form_submission_method = 'whatsapp')
    form_whatsapp_number = models.CharField(
        max_length=20,
        default="60122992909",
        help_text="WhatsApp number (without + sign) for form submissions"
    )
    form_whatsapp_message_template = models.TextField(
        default="Hi! I'm interested in getting a quote for air conditioning service.\n\n*Name:* {name}\n*Email:* {email}\n*Phone:* {phone}\n*Budget:* {budget}\n*Location:* {location}\n*Requirements:* {message}\n\nPlease contact me for a free quote. Thank you!",
        help_text="WhatsApp message template. Use {name}, {email}, {phone}, {budget}, {location}, {message} as placeholders"
    )
    form_whatsapp_success_message = models.CharField(
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

    # Content blocks here
    usp_content_blocks = StreamField([
        ('heading', blocks.CharBlock(classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('html', blocks.RawHTMLBlock()),

        ('call_to_action', CallToActionBlock()),

    ], blank=True, null=True, use_json_field=True)

    # Content blocks here
    hero_content_blocks = StreamField([
        ('heading', blocks.CharBlock(classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('html', blocks.RawHTMLBlock()),

        ('call_to_action', CallToActionBlock()),
    ], blank=True, null=True, use_json_field=True)

    # Content blocks here
    expertise_content_blocks = StreamField([
        ('heading', blocks.CharBlock(classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('html', blocks.RawHTMLBlock()),

        ('call_to_action', CallToActionBlock()),
    ], blank=True, null=True, use_json_field=True)

    # Content blocks here
    partners_content_blocks = StreamField([
        ('heading', blocks.CharBlock(classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('html', blocks.RawHTMLBlock()),

        ('call_to_action', CallToActionBlock()),
    ], blank=True, null=True, use_json_field=True)

    # Content blocks here
    testimonial_content_blocks = StreamField([
        ('heading', blocks.CharBlock(classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('html', blocks.RawHTMLBlock()),

        ('call_to_action', CallToActionBlock()),
    ], blank=True, null=True, use_json_field=True)

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
            FieldPanel('form_submission_method'),
        ], heading="Contact Form Settings"),
        InlinePanel('form_fields', heading="Form Fields", 
                   help_text="Add form fields for the contact form (only used when Email method is selected)"),
        MultiFieldPanel([
            FieldPanel('form_whatsapp_number'),
            FieldPanel('form_whatsapp_message_template'),
            FieldPanel('form_whatsapp_success_message'),
        ], heading="WhatsApp Settings (only used when WhatsApp method is selected)"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6'),
                FieldPanel('to_address', classname='col6'),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings (only used when Email method is selected)"),
        FormSubmissionsPanel(),
        InlinePanel('thank_you_settings', heading="Thank You Page Settings", 
                   help_text="Customize the thank you page content and layout", 
                   max_num=1),
        FieldPanel('hero_content_blocks')
    ]
    
    services_panels = [
        MultiFieldPanel([
            FieldPanel('services_title'),
            FieldPanel('services_subtitle'),
        ], heading="Services Section"),
        InlinePanel('usp_features', heading="USP Features", min_num=1),
        FieldPanel('usp_content_blocks'),
    ]
    
    stats_panels = [
        MultiFieldPanel([
            FieldPanel('stats_title'),
            FieldPanel('stats_subtitle'),
        ], heading="Statistics Section"),
        InlinePanel('statistics', heading="Statistics", min_num=1),
        FieldPanel('expertise_content_blocks'),
    ]
    
    partners_panels = [
        MultiFieldPanel([
            FieldPanel('partners_title'),
            FieldPanel('partners_subtitle'),
            # InlinePanel('home_images', label="Home Images"),
        ], heading="Partners Section"),
        InlinePanel('brand_partners', heading="Brand Partners", min_num=1),
        FieldPanel('partners_content_blocks'),
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
        FieldPanel('testimonial_content_blocks'),
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
                'name': section.section_name
            }
        return sections
    
    def get_thank_you_settings(self):
        """Return the thank you page settings or create default settings"""
        settings = self.thank_you_settings.first()
        if not settings:
            # Create default settings if none exist
            settings = ThankYouPageSettings(
                page=self,
                thank_you_title="Thank You!",
                thank_you_message="Your inquiry has been successfully submitted. We've received your message and will get back to you as soon as possible.",
                info_box_title="What Happens Next?",
                info_box_content="<p>✓ We'll review your inquiry within 24 hours</p><p>✓ Our team will contact you via email or phone</p><p>✓ We'll provide a detailed quote and answer all your questions</p>",
                home_button_text="Back to Home",
                submit_another_button_text="Submit Another Inquiry",
                contact_section_title="Need Immediate Assistance?",
                phone_link_text="Call Us",
                whatsapp_link_text="WhatsApp Us",
                show_info_box=True,
                show_contact_section=True
            )
        return settings
    
    def serve(self, request, *args, **kwargs):
        """
        Override serve to handle form submissions based on the selected method.
        If WhatsApp is selected, render the page normally (JavaScript handles submission).
        If Email is selected, use Wagtail's built-in email form handling and send via Mailtrap.
        """
        from django.shortcuts import render
        from django.conf import settings
        from decouple import config
        import mailtrap as mt
        
        # If form submission method is WhatsApp, just render the page
        # JavaScript will handle the form submission
        if self.form_submission_method == 'whatsapp':
            return super(AbstractEmailForm, self).serve(request, *args, **kwargs)
        
        # If form submission method is Email, handle it with Wagtail's form system
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)
            
            if form.is_valid():
                # Save the form submission to database
                form_submission = self.process_form_submission(form)
                
                # Send to Zapier webhook
                try:
                    # pass the request so site-specific settings can be resolved
                    self.send_to_zapier_webhook(form, request=request)
                except Exception as e:
                    # Log the error but don't fail the submission
                    print(f"Error sending to Zapier webhook: {str(e)}")
                
                # Send email via Mailtrap
                try:
                    self.send_via_mailtrap(form)
                except Exception as e:
                    # Log the error but don't fail the submission
                    print(f"Error sending email via Mailtrap: {str(e)}")
                
                # Render the thank you page
                return self.render_landing_page(request, form_submission, *args, **kwargs)
        else:
            form = self.get_form(page=self, user=request.user)
        
        context = self.get_context(request)
        context['form'] = form
        return render(request, self.get_template(request), context)
    
    def send_to_zapier_webhook(self, form, request=None):
        """
        Send form submission to Zapier webhook.

        Tries to resolve `WebhookSettings` using the provided `request` (recommended).
        Falls back to resolving settings from the page's site when request is not
        available. If settings are missing or disabled, the method returns silently.
        """
        import requests
        from django.utils import timezone

        # Resolve webhook settings. Prefer request (site-aware), fall back to page site.
        webhook_settings = None
        try:
            if request is not None:
                webhook_settings = WebhookSettings.for_request(request)
            else:
                site = self.get_site()
                if site is not None:
                    webhook_settings = WebhookSettings.for_site(site)
        except Exception:
            # If settings can't be resolved, leave webhook_settings as None
            webhook_settings = None

        # Check if webhook is enabled and URL is configured
        if not webhook_settings or not getattr(webhook_settings, 'webhook_enabled', False) or not getattr(webhook_settings, 'zapier_webhook_url', ''):
            # Nothing to do - Zapier integration disabled or not configured
            print("Zapier webhook is disabled or URL not configured for this site")
            return None

        # Collect form data
        form_data = {
            'form type' : 'contact',
            'source': 'Seng Leong Engineering Website'
        }

        # Add all form fields
        for field in self.form_fields.all():
            field_key = field.clean_name
            field_value = form.cleaned_data.get(field_key, '')
            form_data[field.label] = field_value

        # Send POST request to Zapier webhook
        response = requests.post(
            webhook_settings.zapier_webhook_url,
            json=form_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        # Raise exception if request failed
        response.raise_for_status()

        return response
    
    def send_via_mailtrap(self, form):
        """
        Send form submission via Mailtrap SDK
        """
        from decouple import config
        import mailtrap as mt
        from django.utils import timezone
        
        # Get Mailtrap API token from environment
        api_token = config('MAILTRAP_API_TOKEN', default='')
        if not api_token:
            raise ValueError("MAILTRAP_API_TOKEN not configured in .env file")
        
        # Collect form data - iterate through the page's form fields
        form_data = {}
        for field in self.form_fields.all():
            # Get the field's clean_name which is used as the form field key
            field_key = field.clean_name
            # Get the value from cleaned_data
            field_value = form.cleaned_data.get(field_key, '')
            # Use the label as the display name
            form_data[field.label] = field_value
        
        # Create HTML email content
        html_content = self.generate_email_html(form_data)
        text_content = self.generate_email_text(form_data)
        
        # Initialize Mailtrap client
        client = mt.MailtrapClient(token=api_token)
        
        # Create the email
        mail = mt.Mail(
            sender=mt.Address(email=self.from_address or "noreply@sengleongaircond.com.my", name="Seng Leong Website"),
            to=[mt.Address(email=self.to_address)],
            subject=self.subject or f"New Contact Form Submission from {form_data.get('Name', 'Website')}",
            text=text_content,
            html=html_content,
            category="Contact Form Submission"
        )
        
        # Send the email
        client.send(mail)
    
    def generate_email_html(self, form_data):
        """Generate beautiful HTML email template"""
        from django.utils import timezone
        
        fields_html = ""
        for field_name, field_value in form_data.items():
            if field_value:
                fields_html += f"""
                <div class="field">
                    <div class="label">{field_name}:</div>
                    <div class="value">{field_value}</div>
                </div>
                """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #1a237e 0%, #0097a7 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border: 1px solid #ddd;
                }}
                .field {{
                    margin: 15px 0;
                    padding: 15px;
                    background: white;
                    border-left: 4px solid #0097a7;
                    border-radius: 4px;
                }}
                .label {{
                    font-weight: bold;
                    color: #1a237e;
                    margin-bottom: 5px;
                    text-transform: capitalize;
                }}
                .value {{
                    color: #555;
                }}
                .footer {{
                    background: #1a237e;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 0 0 10px 10px;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1 style="margin: 0;">New Contact Form Submission</h1>
                <p style="margin: 10px 0 0 0;">from Seng Leong Engineering Website</p>
            </div>
            
            <div class="content">
                {fields_html}
                
                <div class="field">
                    <div class="label">Submitted At:</div>
                    <div class="value">{timezone.now().strftime('%d %B %Y, %I:%M %p %Z')}</div>
                </div>
            </div>
            
            <div class="footer">
                <p>This email was sent from the contact form on sengleongaircond.com</p>
                <p>Seng Leong Engineering Sdn Bhd - Air Conditioning Services Klang Valley</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def generate_email_text(self, form_data):
        """Generate plain text email"""
        from django.utils import timezone
        
        text = "NEW CONTACT FORM SUBMISSION\n\n"
        for field_name, field_value in form_data.items():
            if field_value:
                text += f"{field_name}: {field_value}\n"
        
        text += f"\nSubmitted at: {timezone.now().strftime('%d %B %Y, %I:%M %p %Z')}\n"
        text += "\n---\nThis email was sent from the contact form on sengleongaircond.com\n"
        text += "Seng Leong Engineering Sdn Bhd\n"
        
        return text




