pip install -r requirements.txt
python manage.py collectstatic --no-input
# python manage.py compilemessages -l ne -l en
python manage.py migrate --no-input
gunicorn sakchyam.wsgi:application --bind 0.0.0.0:8000 --workers 5