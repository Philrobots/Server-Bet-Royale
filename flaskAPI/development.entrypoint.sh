#! bin/sh
gunicorn --threads 5 --reload --bind 0.0.0.0:8000 --chdir /flask run:app