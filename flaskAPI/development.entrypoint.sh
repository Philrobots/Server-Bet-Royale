#! bin/sh
gunicorn -w 1 --threads=12 -worker-class=gthread --limit-request-line 0  --bind 0.0.0.0:8000 --chdir /flask run:app