web: python manage.py collectstatic --no-input && python manage.py migrate && python manage.py seed_showcase && gunicorn config.wsgi:application --log-file -
