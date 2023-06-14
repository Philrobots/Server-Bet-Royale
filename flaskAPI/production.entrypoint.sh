#! bin/sh
gunicorn --worker-class=gevent --worker-connections=1000 --workers=2  --reload --timeout 600 --limit-request-line 0  --bind 0.0.0.0:8000 --chdir /flask run:app