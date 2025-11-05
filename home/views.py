from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from decouple import config
import json
from mailtrap import Mail, Address, MailtrapClient


@require_http_methods(["POST"])
@csrf_exempt  # You might want to handle CSRF properly in production
def submit_contact_form(request):
    """
    Handle contact form submissions via email using Mailtrap SDK
    """
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        
        # Extract form fields
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        budget = data.get('budget', '')
        location = data.get('location', '')
        message = data.get('message', '')
        
        # Validate required fields
        if not all([name, email, phone, location]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields.'
            }, status=400)
        
        # Get Mailtrap API token from environment
        api_token = config('MAILTRAP_API_TOKEN', default='')
        recipient_email = config('CONTACT_EMAIL', default='info@sengleongaircond.com')
        
        if not api_token:
            return JsonResponse({
                'success': False,
                'message': 'Email service not configured. Please try WhatsApp instead.'
            }, status=500)
        
        # Create the email content
        html_content = f"""
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
                .icon {{
                    display: inline-block;
                    margin-right: 8px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1 style="margin: 0;">🎯 New Quote Request</h1>
                <p style="margin: 10px 0 0 0;">from Seng Leong Engineering Website</p>
            </div>
            
            <div class="content">
                <div class="field">
                    <div class="label">👤 Customer Name:</div>
                    <div class="value">{name}</div>
                </div>
                
                <div class="field">
                    <div class="label">📧 Email Address:</div>
                    <div class="value"><a href="mailto:{email}">{email}</a></div>
                </div>
                
                <div class="field">
                    <div class="label">📱 Phone Number:</div>
                    <div class="value"><a href="tel:{phone}">{phone}</a></div>
                </div>
                
                <div class="field">
                    <div class="label">📍 Location:</div>
                    <div class="value">{location}</div>
                </div>
                
                {f'''
                <div class="field">
                    <div class="label">💰 Budget:</div>
                    <div class="value">{budget}</div>
                </div>
                ''' if budget else ''}
                
                {f'''
                <div class="field">
                    <div class="label">💬 Additional Message:</div>
                    <div class="value">{message}</div>
                </div>
                ''' if message else ''}
                
                <div class="field">
                    <div class="label">🕐 Submitted At:</div>
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
        budget_text = f"Budget: {budget}" if budget else ""

        message_text = f"Additional Message:\n{message}" if message else ""

        # Plain text version for email clients that don't support HTML
        text_content = f"""
        NEW QUOTE REQUEST
        
        Customer Details:
        Name: {name}
        Email: {email}
        Phone: {phone}
        Location: {location}
        Budget: {budget_text}

        Additional Message: 
        {message_text}
                
        Submitted at: {timezone.now().strftime('%d %B %Y, %I:%M %p %Z')}
        
        ---
        This email was sent from the contact form on sengleongaircond.com
        Seng Leong Engineering Sdn Bhd
        """
        
        # Initialize Mailtrap client
        client = MailtrapClient(token=api_token)

        # Create the email
        mail = Mail(
            sender=Address(email="noreply@sengleongaircond.com.my", name="Seng Leong Website"),
            to=[Address(email=recipient_email)],
            subject=f"New Quote Request from {name} - {location}",
            text=text_content,
            html=html_content,
            category="Contact Form Submission"
        )
        
        # Send the email
        response = client.send(mail)
        
        print(response)
        return JsonResponse({
            'success': True,
            'message': 'Thank you! Your inquiry has been sent successfully. We will get back to you soon.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format.'
        }, status=400)
    
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while sending your message. Please try WhatsApp instead or contact us directly.'
        }, status=500)


def thank_you_page(request):
    """
    Render the thank you page after successful form submission
    """
    from django.shortcuts import render
    from .models import HomePage
    
    # Get the HomePage instance (there's only one with max_count=1)
    try:
        page = HomePage.objects.live().first()
    except HomePage.DoesNotExist:
        page = None
    
    # Render the thank you template with page context
    context = {
        'page': page,
    }
    
    return render(request, 'home/home_page_landing.html', context)
