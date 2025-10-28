from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList, FieldRowPanel
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
# Create your models here.


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete = models.CASCADE,
        related_name ='form_fields'
    )


class ContactPage(AbstractEmailForm):

    parent_page_types = [
        'home.HomePage',
        'wagtailcore.Page'  # Allow creation under root page too
    ]
    
    template = "contact/contact_page.html"
    
    intro = RichTextField(blank=True)

    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels  + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        FieldPanel('thank_you_text'),
        InlinePanel('form_fields', label= 'Form Fields'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6'),
                FieldPanel('to_address', classname='col6')
            ])
        ]),
        FieldPanel('subject')
        ]
    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Pages"