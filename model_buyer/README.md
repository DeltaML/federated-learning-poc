# Federated learning - Model Buyer


## Installing

A step by step series that tell you how to get a development env running



```
git clone git@github.com:DeltaML/federated-learning-poc.git
cd federated-learning-poc/
python3 -m venv venv
source venv/bin/activate
pip install -r model_buyer/requirements.txt
```

## Run

### Using command line
``` bash
    gunicorn -b "0.0.0.0:9090" --chdir model_buyer/ wsgi:app --preload
``` 


### Using Pycharm

	Script Path: .../model_buyer/virtualenv/bin/gunicorn
	Parameters: -b "0.0.0.0:9090" wsgi:app --preload
	Working directory: ../model_buyer


## Usage 
 
### Make model from federated trainer

``` bash
curl -v -H "Content-Type: application/json" -X POST "http://localhost:9090/model"
```

### Get prediction

``` bash
curl -v -H "Content-Type: application/json" -X GET "http://localhost:9090/prediction"
```



## Model buyer configuration

``` python3

config = {
    'server_register_url': "http://cte_federated_trainer:8080/model",
    'key_length': 1024,
    'port': 9090,
    'active_encryption': False
}
```

### Configuration details

- server_register_url: __TODO__
- key_length: __TODO__
- port: __TODO__
- active_encryption: __TODO__
