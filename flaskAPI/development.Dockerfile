FROM python:3.11-slim
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ADD . /flask
WORKDIR /flask
RUN apt update
RUN apt install -y curl
RUN pip3 install -r requirements.txt
ENV MONGODB_CONNECTION_STRING THIS_SHOULD_LEAD_TO_DB_SET_IT_IN_DOCKERCOMPOSE
ENTRYPOINT ["bash", "development.entrypoint.sh"]