# Contact Form Enhancement - WhatsApp & Email Toggle

This update adds a toggleable contact form that allows users to choose between WhatsApp and Email submission methods.

## Features Added

1. **Toggle between WhatsApp and Email** - Users can switch between contact methods
2. **Email integration with Mailtrap SDK** - Professional email delivery service
3. **Environment variable support** - Secure configuration management
4. **Beautiful HTML email templates** - Professional-looking emails
5. **Admin panel controls** - Configure all settings from Wagtail admin

## Installation Steps

### 1. Install Required Packages

```bash
cd /Applications/XAMPP/xamppfiles/code/whisttle/clients/sengleongaircond
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit the `.env` file and add your Mailtrap API token:

```env
MAILTRAP_API_TOKEN=your_actual_api_token_here
CONTACT_EMAIL=info@sengleongaircond.com
```

**To get your Mailtrap API token:**
1. Go to https://mailtrap.io/
2. Sign up or log in
3. Navigate to Settings → API Tokens
4. Generate a new token with "Email Sending" permissions
5. Copy the token to your `.env` file

### 3. Update Settings to Use Environment Variables

Edit `base/settings/base.py` or `base/settings/dev.py`:

```python
from decouple import config

# Add at the top after imports
SECRET_KEY = config('SECRET_KEY', default='your-default-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)
```

### 4. Run Migrations

```bash
python manage.py makemigrations home
python manage.py migrate
```

### 5. Restart the Server

```bash
python manage.py runserver
```

## Configuration in Wagtail Admin

1. Go to `/admin/`
2. Navigate to Pages → Home
3. Click on the "Hero Section" tab
4. Configure the contact form:
   - **Contact Form Settings:**
     - Enable email submission option
     - Choose default contact method (WhatsApp or Email)
   - **WhatsApp Settings:**
     - WhatsApp number
     - Message template
     - Success message
   - **Email Settings:**
     - Email recipient address
     - Email success message

## Testing

### Test WhatsApp Submission:
1. Go to your homepage
2. Fill in the contact form
3. Click "Send via WhatsApp"
4. Should open WhatsApp with pre-filled message

### Test Email Submission:
1. Go to your homepage
2. Click the "Email" toggle button
3. Fill in the contact form
4. Click "Send Email Inquiry"
5. Check your Mailtrap inbox for the email

## Troubleshooting

### Email not sending:
- Check that `MAILTRAP_API_TOKEN` is set correctly in `.env`
- Verify the token has "Email Sending" permissions
- Check browser console for errors
- Check Django logs for detailed error messages

### Toggle not working:
- Clear browser cache
- Check browser console for JavaScript errors
- Ensure the page was saved and published in Wagtail admin

### CSRF token errors:
- Make sure Django's CSRF middleware is enabled
- Check that cookies are enabled in the browser

## File Changes Summary

### New Files:
- `home/views.py` - Email submission handler
- `.env.example` - Environment variable template
- This `README.md`

### Modified Files:
- `requirements.txt` - Added mailtrap and python-decouple
- `base/urls.py` - Added API endpoint for form submission
- `home/models.py` - Added email-related fields to HomePage
- `home/templates/home/home_page.html` - Added toggle UI and email handling

## Security Notes

1. Never commit your `.env` file to git
2. Use proper CSRF protection in production
3. Validate all form inputs on the server side
4. Use environment variables for all sensitive data
5. Enable HTTPS in production

## Support

For issues or questions, contact the development team.
