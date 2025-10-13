from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class CallToActionBlock(blocks.StructBlock):
    button_text = blocks.CharBlock(max_length=50)
    button_redirect = blocks.ChoiceBlock(
        choices = [
        ('#hero', 'Hero Section'),
        ('#usp-section', 'USP Features Section'),
        ('#expertise-section', 'Statistics/Expertise Section'),
        ('#partners', 'Partners Section'),
        ('#testimonials', 'Google Reviews Section')
    ]
    )
    background_color = blocks.ChoiceBlock(choices=[
        ('#0A1F44', 'primary-navy'),
        ('#FFFFFF', 'white'),
        ('#3B82F6', 'sky-blue'),
        ('#F4F6FA', 'light-gray'),
        ('#1E293B', 'dark-text'),
        ('#06B6D4', 'bright-cyan'),
        ('#1E3A8A', 'dark-navy-hover'),
        ('#FACC15', 'yellow-highlight'),
    ])
    text_color = blocks.ChoiceBlock(choices=[
        ('white', 'White'),
        ('black', 'Black'),
        ('gray', 'Gray'),
    ])
    
    class Meta:
        template = 'blocks/call_to_action.html'
        icon = 'pick'
        label = 'Call to Action'

