FROM python:3

RUN apt-get update -yq \
    && apt-get install curl gnupg -yq \
    && curl -sL https://deb.nodesource.com/setup_8.x | bash \
    && apt-get install nodejs -yq
WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./model_buyer
ADD ./commons ./commons
ADD ./model_buyer ./model_buyer

RUN npm install --prefix ./model_buyer/ui && npm run build --prefix ./model_buyer/ui
RUN pip install -r ./model_buyer/requirements.txt

EXPOSE 9090
CMD [ "gunicorn", "-b", "0.0.0.0:9090", "wsgi:app", "--chdir", "model_buyer/", "--preload"]