FROM python:2.7.10
MAINTAINER Friedrich Lindenberg <pudo@occrp.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq && apt-get install -y -q --no-install-recommends \
        curl git python2.7 python-pip build-essential python-dev ruby-sass \
        libxml2-dev libxslt1-dev libpq-dev curl apt-utils ca-certificates \
  && apt-get clean

RUN curl --silent --location https://deb.nodesource.com/setup_0.12 | sh
RUN apt-get install --yes nodejs && curl -L https://www.npmjs.org/install.sh | sh
RUN npm install -g bower uglifyjs

COPY . /schwifty
WORKDIR /schwifty

ENV SCHWIFTY_SETTINGS /schwifty/contrib/docker_settings.py
RUN pip install functools32 gunicorn && pip install -r requirements.txt -e .
RUN rm -rf .git && bower --allow-root install

EXPOSE 8000
