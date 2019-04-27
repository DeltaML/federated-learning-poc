FROM python:3


WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./server
ADD ./commons ./commons
ADD ./server ./server
RUN pip install -r ./server/requirements.txt

EXPOSE 8080
CMD [ "gunicorn", "-b", "0.0.0.0:8080", "wsgi:app", "--chdir", "server/", "--preload"]