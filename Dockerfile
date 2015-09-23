FROM python:2-onbuild
MAINTAINER Friedrich Lindenberg <pudo@occrp.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq && apt-get install -y -q --no-install-recommends \
        curl git python2.7 python-pip build-essential python-dev \
        libxml2-dev libxslt1-dev libpq-dev curl apt-utils ca-certificates \
  && apt-get clean && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

RUN curl --silent --location https://deb.nodesource.com/setup_0.12 | sh
RUN apt-get install --yes nodejs && curl -L https://www.npmjs.org/install.sh | sh
RUN npm install -g bower

ADD . /schwifty
WORKDIR /schwifty

ENV SCHWIFTY_SETTINGS /schwifty/contrib/docker_settings.py
RUN pip install functools32 && pip install -r /schwifty/requirements.txt -e /schwifty

EXPOSE 8000
