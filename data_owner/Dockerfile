# ---- Base ----
# ---- Python ----
FROM python:3 AS base-python
# Create app directory
WORKDIR /app
# ---- Node ----
FROM node:8.16.0-alpine AS base-node
# Create app directory
WORKDIR /app

# ---- Dependencies ----

# ---- Python ----
FROM base-python AS dependencies-python
RUN mkdir -p ./data_owner
COPY ./data_owner/requirements.txt ./data_owner
# install app dependencies
RUN pip install -r ./data_owner/requirements.txt

# ---- Node ----
FROM base-node AS dependencies-node
RUN mkdir -p ./data_owner/ui
COPY ./data_owner/ui/package.json ./data_owner/ui
RUN npm install --prefix ./data_owner/ui

# ---- Copy Files/Build ----
# ---- Python ----
FROM dependencies-python AS build-python
WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./data_owner
ADD ./commons ./commons
ADD ./data_owner ./data_owner
# ---- Node ----
FROM dependencies-node AS build-node
RUN mkdir -p ./data_owner/ui
ADD ./data_owner/ui ./data_owner/ui
RUN npm run build --prefix ./data_owner/ui

# ---- Final build ----
FROM alpine AS build
WORKDIR /app
COPY --from=build-python /app/data_owner/ ./data_owner
COPY --from=build-python /app/commons/ ./commons
COPY --from=build-node /app/data_owner/ui/build ./data_owner/ui/build

# --- Release ----

FROM python:3 AS release
# Create app directory
WORKDIR /app

COPY --from=dependencies-python /app/data_owner/requirements.txt ./
COPY --from=dependencies-python /root/.cache /root/.cache

# Install app dependencies
RUN pip install -r requirements.txt
COPY --from=build /app/ ./
EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app", "--chdir", "data_owner/", "--preload"]
