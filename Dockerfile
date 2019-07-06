FROM python:3.6

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./hakathon

WORKDIR /app/hakathon/

EXPOSE 80
CMD ["gunicorn", "hakathon.wsgi", "-w", "4", "-b 0.0.0.0:80", "--env", "DJANGO_SETTINGS_MODULE=hakathon.settings", "--pythonpath=/usr/local/lib/python3.6/site-packages/", "--preload"]
