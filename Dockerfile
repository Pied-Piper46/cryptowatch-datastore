FROM python:3.9.10-slim-buster

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get -y install cron
RUN pip install --no-cache-dir -r requirements.txt

ADD cron.conf /etc/cron.d/mycron

RUN chmod 0644 /etc/cron.d/mycron

RUN crontab /etc/cron.d/mycron

RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log