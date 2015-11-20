FROM occrp/flask-node-base
MAINTAINER Friedrich Lindenberg <pudo@occrp.org>

COPY . /spindle
WORKDIR /spindle

ENV SPINDLE_SETTINGS /spindle/contrib/docker_settings.py
RUN pip install functools32 gunicorn && pip install -r requirements.txt \
    && pip install -e .
RUN rm -rf .git && bower --allow-root install

EXPOSE 8000
