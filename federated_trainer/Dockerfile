FROM python:3


WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./cte_federated_trainer
ADD ./commons ./commons
ADD ./cte_federated_trainer ./cte_federated_trainer
RUN pip install -r ./cte_federated_trainer/requirements.txt

EXPOSE 8080
CMD [ "gunicorn", "-b", "0.0.0.0:8080", "wsgi:app", "--chdir", "cte_federated_trainer/", "--preload"]