FROM python:3


WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./client
ADD ./commons ./commons
ADD ./client ./client
RUN pip install -r ./client/requirements.txt

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app", "--chdir", "client/", "--preload"]