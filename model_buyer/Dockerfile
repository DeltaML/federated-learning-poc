FROM python:3 AS base
# Create app directory
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
RUN mkdir -p ./model_buyer
COPY ./model_buyer/requirements.txt ./model_buyer
# install app dependencies
RUN pip install -r ./model_buyer/requirements.txt


# ---- Copy Files/Build ----
FROM dependencies AS build
WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./model_buyer
ADD ./commons ./commons
ADD ./model_buyer ./model_buyer

# --- Release ----

FROM python:3 AS release
# Create app directory
WORKDIR /app

COPY --from=dependencies /app/model_buyer/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache

# Install app dependencies
RUN pip install -r requirements.txt
COPY --from=build /app/ ./
EXPOSE 9090
CMD [ "gunicorn", "-b", "0.0.0.0:9090", "wsgi:app", "--chdir", "model_buyer/", "--preload"]
