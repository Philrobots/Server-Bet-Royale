#! bin/sh
gunicorn --worker-class=gevent --worker-connections=1000 --workers=3  --reload --timeout 600 --bind 0.0.0.0:8000 --chdir /flask run:app