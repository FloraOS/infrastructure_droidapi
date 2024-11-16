FROM python:3.11-slim
LABEL authors=["0xf104a"]

WORKDIR /opt

RUN apt update -y && apt install -y libpq-dev python3-dev gcc

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

COPY src/droidapi /opt/droidapi

ENV FLASK_APP=droidapi
ENV FLASK_ENV=production

EXPOSE 8000

ENTRYPOINT uwsgi --http-socket :8000\
  -w droidapi:app\
  --processes 1\
  --threads 1\
  --harakiri 1200\
  --post-buffering 524288 \
  --buffer-size 65535