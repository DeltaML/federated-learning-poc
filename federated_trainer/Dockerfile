# ---- Base ----
# ---- Python ----
FROM python:3 AS base-python
# Create app directory
WORKDIR /app


# ---- Dependencies ----

# ---- Python ----
FROM base-python AS dependencies-python
RUN mkdir -p ./federated_trainer
COPY ./federated_trainer/requirements.txt ./federated_trainer
# install app dependencies
RUN pip install -r ./federated_trainer/requirements.txt

# ---- Copy Files/Build ----
# ---- Python ----
FROM dependencies-python AS build-python
WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./federated_trainer
ADD ./commons ./commons
ADD ./federated_trainer ./federated_trainer

# ---- Final build ----
FROM alpine AS build
WORKDIR /app
COPY --from=build-python /app/federated_trainer/ ./federated_trainer
COPY --from=build-python /app/commons/ ./commons

# --- Release ----

FROM python:3 AS release
# Create app directory
WORKDIR /app

COPY --from=dependencies-python /app/federated_trainer/requirements.txt ./
COPY --from=dependencies-python /root/.cache /root/.cache

# Install app dependencies
RUN pip install -r requirements.txt
COPY --from=build /app/ ./
EXPOSE 8080
CMD [ "gunicorn", "-b", "0.0.0.0:8080", "wsgi:app", "--chdir", "federated_trainer/", "--preload"]
