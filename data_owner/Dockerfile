FROM python:3

RUN apt-get update -yq \
    && apt-get install curl gnupg -yq \
    && curl -sL https://deb.nodesource.com/setup_8.x | bash \
    && apt-get install nodejs -yq

WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./data_owner
ADD ./commons ./commons
ADD ./data_owner ./data_owner


RUN npm install && npm run-script build --prefix ./data_owner/ui
RUN pip install -r ./data_owner/requirements.txt
EXPOSE 5000

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app", "--chdir", "data_owner/", "--preload"]
