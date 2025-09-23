# Seng Leong Engineering - Air Conditioning Website

A professional Django/Wagtail CMS website for Seng Leong Engineering Sdn Bhd, specializing in air conditioning installation, repair, and maintenance services in Klang Valley, Malaysia.

## 🌟 Features

### 🎯 WhatsApp Integration

- **Smart Contact Form**: Automatically formats and sends inquiries via WhatsApp
- **CMS-Controlled Numbers**: Admin can change WhatsApp recipient numbers from the backend
- **Custom Message Templates**: Configurable message templates with placeholder support
- **Phone Number Cleaning**: Handles Unicode characters and ensures clean WhatsApp URLs
- **Multiple WhatsApp Entry Points**: Form submission, footer links, and floating button

### 🏢 Business Features

- **Multi-Section Homepage**: Hero, services, statistics, partners, testimonials, contact
- **Brand Partner Showcase**: Carousel display of authorized air conditioning brands
- **Service Statistics**: Animated counters for business achievements
- **Customer Testimonials**: Integrated Google Reviews via Elfsight
- **USP Features**: Customizable unique selling points with FontAwesome icons

### 📱 Technical Features

- **Responsive Design**: Mobile-first approach with smooth animations
- **SEO Optimized**: Meta tags, structured data, Open Graph, Twitter Cards
- **Performance Focused**: Preloaded critical resources, optimized images
- **Accessibility**: ARIA labels, semantic HTML, keyboard navigation
- **Analytics Ready**: Google Analytics event tracking placeholders

## 🛠️ Technology Stack

- **Backend**: Django 4.x + Wagtail CMS
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Inter)
- **External Services**:
  - Elfsight (Google Reviews widget)
  - Google Maps (embedded location)
  - WhatsApp Business API

## 📁 Project Structure

```
sengleongaircond/
├── base/                          # Django project settings
│   ├── settings/                  # Environment-specific settings
│   │   ├── base.py               # Base settings
│   │   ├── dev.py                # Development settings
│   │   └── production.py         # Production settings
│   ├── static/                   # Global static files
│   └── templates/                # Global templates
├── home/                         # Main application
│   ├── models.py                 # Wagtail page models
│   ├── static/                   # App-specific static files
│   ├── templates/home/           # App templates
│   │   └── home_page.html        # Main homepage template
│   └── migrations/               # Database migrations
├── media/                        # User-uploaded files
├── search/                       # Search functionality
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Whisttle/sengleongaircond.git
cd sengleongaircond
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py migrate
```

5. **Create superuser**

```bash
python manage.py createsuperuser
```

6. **Collect static files**

```bash
python manage.py collectstatic
```

7. **Run development server**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the website and `http://127.0.0.1:8000/admin` for the CMS admin.

## ⚙️ Configuration

### Environment Settings

- **Development**: Uses `base/settings/dev.py`
- **Production**: Uses `base/settings/production.py`

### WhatsApp Configuration

Configure these fields in the Wagtail admin under Homepage:

- **WhatsApp Number**: `form_whatsapp_number` (digits only, no + sign)
- **Message Template**: `form_whatsapp_message_template` (supports placeholders)
- **Success Message**: `form_success_message`

#### Message Template Placeholders:

- `{name}` - Customer's full name
- `{email}` - Customer's email address
- `{phone}` - Customer's phone number
- `{budget}` - Project budget
- `{location}` - Service location
- `{message}` - Additional comments

### Content Management

All content is manageable through the Wagtail admin interface:

#### Hero Section

- Title, description, background image
- Form configuration (title, subtitle, WhatsApp settings)

#### Services Section

- Section title and subtitle
- USP features (icon, title, description)

#### Statistics Section

- Section title and subtitle
- Statistics items (number, label)

#### Partners Section

- Section title and subtitle
- Brand partner logos with alt text

#### Contact Section

- Company information
- Address details
- Social media links
- Google Maps embed

#### SEO Settings

- Meta description and keywords
- Structured data (automatically generated)

## 🎨 Customization

### Adding New USP Features

1. Go to Wagtail admin → Pages → Homepage
2. Navigate to "Services" tab
3. Add new USP Feature with:
   - Icon class (FontAwesome)
   - Title
   - Description

### Adding Brand Partners

1. Go to Wagtail admin → Pages → Homepage
2. Navigate to "Partners" tab
3. Upload logo image and add alt text

### Updating Statistics

1. Go to Wagtail admin → Pages → Homepage
2. Navigate to "Statistics" tab
3. Add number (e.g., "3000+", "90%") and label

## 🔧 Development

### Running in Development Mode

```bash
export DJANGO_SETTINGS_MODULE=base.settings.dev
python manage.py runserver
```

### Creating New Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Development

```bash
python manage.py collectstatic --noinput
```

## 🚀 Deployment

### Production Settings

Ensure these environment variables are set:

- `DJANGO_SETTINGS_MODULE=base.settings.production`
- `SECRET_KEY` - Django secret key
- `DEBUG=False`
- Database configuration variables

### Static Files

```bash
python manage.py collectstatic --noinput
```

### Database

```bash
python manage.py migrate
```

## 📱 WhatsApp Integration Details

### Form Submission Flow

1. User fills out contact form
2. JavaScript validates required fields
3. Form data is formatted using CMS template
4. WhatsApp URL is generated with cleaned phone number
5. User is redirected to WhatsApp with pre-filled message
6. Success message is displayed

### Phone Number Cleaning

The system automatically removes:

- Invisible Unicode characters (e.g., left-to-right marks)
- Spaces, dashes, plus signs
- Non-digit characters

### Message Formatting

Default template if none specified:

```
🎯 *NEW QUOTE REQUEST*

👤 *Customer Details:*
• Name: {name}
• Email: {email}
• Phone: {phone}

📍 *Service Details:*
• Location: {location}
• Budget: {budget}

💬 *Additional Comments:*
{message}

⏰ *Submitted:* [timestamp]

_Please respond to this quote request promptly._
```

## 🔍 SEO Features

- **Meta Tags**: Dynamic title, description, keywords
- **Open Graph**: Social media sharing optimization
- **Twitter Cards**: Twitter sharing optimization
- **Structured Data**: Local business schema markup
- **Canonical URLs**: Prevents duplicate content
- **Geo Tags**: Location-based SEO

## 🎯 Performance Optimizations

- **Lazy Loading**: Images and external scripts
- **Preconnect**: External font and CDN domains
- **Critical CSS**: Above-the-fold styles inlined
- **Image Optimization**: Responsive images with Wagtail
- **Minification**: CSS and JavaScript compression
- **Caching**: Static file caching headers

## 🐛 Troubleshooting

### WhatsApp Links Not Working

1. Check browser console for phone number cleaning logs
2. Verify `form_whatsapp_number` has no invalid characters
3. Ensure number is in international format (e.g., 60123456789)

### Form Not Submitting

1. Check JavaScript console for errors
2. Verify all required fields are filled
3. Check if WhatsApp number is properly configured

### Admin Access Issues

1. Ensure superuser is created: `python manage.py createsuperuser`
2. Check database migrations are up to date
3. Verify admin URLs in `base/urls.py`

## 📞 Support

For technical support or questions about this project:

- **Developer**: Whisttle Team
- **Client**: Seng Leong Engineering Sdn Bhd
- **Project Type**: Business Website with CMS

## 📄 License

This project is proprietary software developed for Seng Leong Engineering Sdn Bhd.

---

**Seng Leong Engineering Sdn Bhd**  
Air Conditioning Services | Klang Valley, Malaysia  
📞 +6012-652 6665 | 🌐 sengleongaircond.com
