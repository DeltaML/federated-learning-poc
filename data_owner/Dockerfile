FROM python:3


WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./data_owner
ADD ./commons ./commons
ADD ./data_owner ./data_owner
RUN apt-get update -yq \
    && apt-get install curl gnupg -yq \
    && curl -sL https://deb.nodesource.com/setup_8.x | bash \
    && apt-get install nodejs -yq
RUN npm install --prefix ./data_owner/ui
RUN pip install -r ./data_owner/requirements.txt
RUN chmod +x ./data_owner/ui/start_client.sh
RUN chmod +x ./data_owner/run-data-owner.sh
EXPOSE 5000
CMD ./data_owner/run-data-owner.sh