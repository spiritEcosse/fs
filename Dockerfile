FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y
# RUN apt-get install -y python-pip python-dev build-essential libpq-dev zip unzip libmysqlclient-dev tzdata rsync ssh
RUN apt-get install -y binutils libproj-dev gdal-bin
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app/
# ENV TZ=Europe/Kiev
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
