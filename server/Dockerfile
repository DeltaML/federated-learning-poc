FROM python:3

WORKDIR /app

RUN mkdir -p ./commons
ADD ./commons ./commons
ADD ./server ./
RUN pip install -r requirements.txt


EXPOSE 5001

CMD [ "gunicorn", "-b", "0.0.0.0:5001", "wsgi:app"]