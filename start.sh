python manage.py makemigrations
python manage.py migrate

read -p "Create super user? (y/n): " make_super

if [[ "$make_super" == 'Y' || "$make_super" == 'y' ]]; then
    echo "Making superuser" 
    python manage.py createsuperuser
else 
    echo 'No superuser'
fi

python manage.py runserver 0.0.0.0:8000