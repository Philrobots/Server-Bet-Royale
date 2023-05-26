FROM python:3.11-slim
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ADD . /flask
WORKDIR /flask
RUN apt update
RUN apt install -y curl
RUN pip3 install -r requirements.txt
ENV FLASK_ENV production
ENV PORT 8000
ENV FLASK_APP run.py
EXPOSE 8000
ENTRYPOINT ["bash", "production.entrypoint.sh"]