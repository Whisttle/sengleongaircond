#!/bin/bash
# filepath: /Applications/XAMPP/xamppfiles/code/whisttle/clients/sengleongaircond/remove_migrations.sh

echo "🔥 Removing all migration files..."

# Remove migration files from all apps (keeping __init__.py files)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Remove migration directories if they're empty (except __pycache__)
find . -path "*/migrations/__pycache__" -type d -exec rm -rf {} + 2>/dev/null

echo "✅ All migration files removed!"
echo ""
echo "📝 Next steps:"
echo "1. python manage.py makemigrations"
echo "2. python manage.py migrate"