FROM python:3


WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./model_buyer
ADD ./commons ./commons
ADD ./model_buyer ./model_buyer
RUN pip install -r ./model_buyer/requirements.txt

EXPOSE 9090
CMD [ "gunicorn", "-b", "0.0.0.0:9090", "wsgi:app", "--chdir", "model_buyer/", "--preload"]