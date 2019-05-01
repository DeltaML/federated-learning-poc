FROM python:3


WORKDIR /app
RUN mkdir -p ./commons
RUN mkdir -p ./cte_model_buyer
ADD ./commons ./commons
ADD ./cte_model_buyer ./cte_model_buyer
RUN pip install -r ./cte_model_buyer/requirements.txt

EXPOSE 9090
CMD [ "gunicorn", "-b", "0.0.0.0:9090", "wsgi:app", "--chdir", "cte_model_buyer/", "--preload"]