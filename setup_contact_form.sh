#!/bin/bash

# Quick Start Script for Contact Form Enhancement
# This script helps you set up the new email form functionality

echo "================================================"
echo "Contact Form Enhancement - Quick Setup"
echo "================================================"
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Activating venv..."
    source ../venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "❌ Failed to activate virtual environment"
        echo "Please activate it manually: source ../venv/bin/activate"
        exit 1
    fi
    echo "✅ Virtual environment activated"
else
    echo "✅ Virtual environment already activated"
fi
echo ""

# Install required packages
echo "📦 Installing required packages..."
pip install -q mailtrap python-decouple
if [ $? -eq 0 ]; then
    echo "✅ Packages installed successfully"
else
    echo "❌ Failed to install packages"
    exit 1
fi
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: You need to add your Mailtrap API token!"
    echo ""
    echo "Steps to get your token:"
    echo "1. Go to https://mailtrap.io/"
    echo "2. Sign up or log in"
    echo "3. Go to Settings → API Tokens"
    echo "4. Create new token with 'Email Sending' permissions"
    echo "5. Edit .env file and paste your token"
    echo ""
    read -p "Press Enter to open .env file in default editor..."
    ${EDITOR:-nano} .env
else
    echo "✅ .env file already exists"
    echo "⚠️  Make sure your MAILTRAP_API_TOKEN is set!"
fi
echo ""

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate
if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed"
    exit 1
fi
echo ""

# Final instructions
echo "================================================"
echo "✨ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. ✅ Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "2. ✅ Configure in admin:"
echo "   - Go to http://127.0.0.1:8000/admin/"
echo "   - Navigate to Pages → Home → Edit"
echo "   - Click 'Hero Section' tab"
echo "   - Enable email and configure settings"
echo ""
echo "3. ✅ Test the form:"
echo "   - Visit your homepage"
echo "   - Try both WhatsApp and Email methods"
echo "   - Check Mailtrap inbox for emails"
echo ""
echo "📚 For detailed documentation, see:"
echo "   - IMPLEMENTATION_SUMMARY.md"
echo "   - CONTACT_FORM_README.md"
echo ""
echo "Happy coding! 🚀"
