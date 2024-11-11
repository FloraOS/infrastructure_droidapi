FROM python:3.11-slim
LABEL authors=["0xf104a"]

WORKDIR /opt

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

COPY src/droidapi /opt/droidapi

ENV FLASK_APP=droidapi
ENV FLASK_ENV=production

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "droidapi:app"]