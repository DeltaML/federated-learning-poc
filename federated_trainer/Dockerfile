FROM python:3


WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./federated_trainer
ADD ./commons ./commons
ADD ./federated_trainer ./federated_trainer
RUN pip install -r ./federated_trainer/requirements.txt

EXPOSE 8080
CMD [ "gunicorn", "-b", "0.0.0.0:8080", "wsgi:app", "--chdir", "federated_trainer/", "--preload"]