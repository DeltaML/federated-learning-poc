FROM python:3

WORKDIR /app

RUN mkdir -p ./commons
ADD ./commons ./commons
ADD ./client ./
RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app", "--preload"]