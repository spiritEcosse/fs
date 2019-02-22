FROM python:2.7
ENV PYTHONUNBUFFERED 1

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y
RUN apt-get install -y build-essential tzdata
RUN echo "Europe/Kiev" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app/



# COPY docker-entrypoint.sh /
# RUN chmod +x /docker-entrypoint.sh
# CMD /docker-entrypoint.sh
