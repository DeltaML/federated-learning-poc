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
 docker build -t federated-learning-client --rm -f client/Dockerfile
```

### Run container

Select _LOCAL_PORT_ number to run some containers
```
docker run --rm -it -p <LOCAL_PORT>:5000 federated-learning-client
```


## Examples

```
curl -H "Content-Type: application/json" -X POST "http://localhost:5000/weights" --data @example-body.json 

```