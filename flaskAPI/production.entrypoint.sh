#! bin/sh
gunicorn --threads 50 --bind 0.0.0.0:8000 --chdir /flask run:app
