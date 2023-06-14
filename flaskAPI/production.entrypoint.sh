#! bin/sh
gunicorn --limit-request-line 0 --workers=2 --bind 0.0.0.0:8000 --chdir /flask run:app
