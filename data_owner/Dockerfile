FROM python:3


WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./data_owner
RUN mkdir -p ./data_owner/dataset
ADD ./commons ./commons
ADD ./data_owner ./data_owner
RUN pip install -r ./data_owner/requirements.txt

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app", "--chdir", "data_owner/", "--preload"]
