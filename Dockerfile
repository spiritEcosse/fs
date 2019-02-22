FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install -y redis-server

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app/
# ENV TZ=Europe/Kiev
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
