FROM python:3

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]