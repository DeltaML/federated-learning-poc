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
RUN mkdir -p ./model_buyer
COPY ./model_buyer/requirements.txt ./model_buyer
# install app dependencies
RUN pip install -r ./model_buyer/requirements.txt

# ---- Node ----
FROM base-node AS dependencies-node
RUN mkdir -p ./model_buyer/ui
COPY ./model_buyer/ui/package.json ./model_buyer/ui
RUN npm install --prefix ./model_buyer/ui

# ---- Copy Files/Build ----
# ---- Python ----
FROM dependencies-python AS build-python
WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./model_buyer
ADD ./commons ./commons
ADD ./model_buyer ./model_buyer
# ---- Node ----
FROM dependencies-node AS build-node
RUN mkdir -p ./model_buyer/ui
ADD ./model_buyer/ui ./model_buyer/ui
RUN npm run build --prefix ./model_buyer/ui

# ---- Final build ----
FROM alpine AS build
WORKDIR /app
COPY --from=build-python /app/model_buyer/ ./model_buyer
COPY --from=build-python /app/commons/ ./commons
COPY --from=build-node /app/model_buyer/ui/build ./model_buyer/ui/build

# --- Release ----

FROM python:3 AS release
# Create app directory
WORKDIR /app

COPY --from=dependencies-python /app/model_buyer/requirements.txt ./
COPY --from=dependencies-python /root/.cache /root/.cache

# Install app dependencies
RUN pip install -r requirements.txt
COPY --from=build /app/ ./
EXPOSE 9090
CMD [ "gunicorn", "-b", "0.0.0.0:9090", "wsgi:app", "--chdir", "model_buyer/", "--preload"]
