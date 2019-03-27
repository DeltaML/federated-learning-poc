FROM python:3

WORKDIR /app

RUN mkdir -p ./commons
ADD ./commons ./commons
ADD ./server ./
RUN pip install -r requirements.txt


EXPOSE 8080

CMD [ "gunicorn", "-b", "0.0.0.0:8080", "wsgi:app", "--preload"]