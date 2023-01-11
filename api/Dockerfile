FROM python:3.11

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y build-essential

ADD requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --default-timeout=100 -r requirements.txt
RUN pip3 install uwsgi


EXPOSE 8888
