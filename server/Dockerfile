FROM python:3

WORKDIR /app

ADD . /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD [ "gunicorn", "-b", "0.0.0.0:5001", "wsgi:app"]