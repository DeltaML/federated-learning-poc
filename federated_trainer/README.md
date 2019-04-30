# Federated learning - Federated Trainer

## Run

### Using command line
``` bash
    gunicorn -b "0.0.0.0:8080" --chdir federated_trainer/ wsgi:app --preload
``` 


### Using Docker
``` bash
    docker build -t federated-learning-federated-trainer --rm -f federated-trainer/Dockerfile
    docker run --rm -it -p 8080:8080federated-learning-federated-trainer
``` 


### Using Pycharm

	Script Path: .../federated_trainer/virtualenv/bin/gunicorn
	Parameters: -b "0.0.0.0:8080" wsgi:app --preload
	Working directory: ../federated_trainer


## Usage 
 
### Register new data owner

``` bash
curl -v -H "Content-Type: application/json" -X POST "http://localhost:8080/dataowner"
```

### Get data owners registered

``` bash
curl -v -H "Content-Type: application/json" -X GET "http://localhost:8080/dataowner"
```

### Train model

``` bash
curl -v -H "Content-Type: application/json" -X POST -d '{"type": "LINEAR_REGRESSION", "call_back_endpoint": "URL_MODEL_BUYER", "call_back_port": 9090,"public_key": "XXXXXXXXXXXXXXXX"}' "http://localhost:8080/model"
```



## Model buyer configuration

``` python3

ENCRYPTION_TYPE = PheEncryption
ACTIVE_ENCRYPTION = False
N_ITER = 100 # El numero de iteraciones aceptables utilizando PheEncryption por ahora es 4
DATA_OWNER_PORT = 5000

```

### Configuration details

- ENCRYPTION_TYPE: __TODO__
- ACTIVE_ENCRYPTION: __TODO__
- N_ITER: __TODO__
- DATA_OWNER_PORT: __TODO__
