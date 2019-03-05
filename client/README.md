# PoF of client over federated learning schema 


## Run local

### Prepare environment and install

```
python3 -m venv venv;
. venv/bin/activate
pip install -r requirements.txt;
```

### Run

```
 gunicorn --bind 0.0.0.0:5000 wsgi:app
```


## Docker

### Build image
```
 docker build -t federated-learning-client --rm .
```

### Run container
```
docker run --rm -it -p 5000:5000 federated-learning-client
```