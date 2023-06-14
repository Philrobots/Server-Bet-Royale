#! bin/sh
gunicorn --workers=2 --threads=5 --worker-class=gthread --limit-request-line 0 --timeout 600  --bind 0.0.0.0:8000 --chdir /flask run:app