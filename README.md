# DeltaML/federated-learning-poc

Repository that contains a Proof of Concept for the implementation of a Federated Learning framework.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites


- [python3](https://www.python.org/download/releases/3.0/)
- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)


**Federated Trainer usage and configuration**

You can see the federated trainer Readme in [Federated Trainer](https://github.com/DeltaML/federated-learning-poc/blob/master/federated_trainer/README.md)

**Data owner usage and configuration**

You can see the Data owner Readme in [Data owner](https://github.com/DeltaML/federated-learning-poc/blob/master/data_owner/README.md)

**Model buyer usage and configuration**

You can see the Model buyer Readme in [Model buyer](https://github.com/DeltaML/federated-learning-poc/blob/master/model_buyer/README.md)

## Deployment

## Using docker-compose

First build 
```
docker-compose build
```

Then run
```
docker-compose up
```

Run and scale data owners
```
docker-compose up --scale cte_data_owner=<N_DATA_OWNERS>
```

## Using Pycharm

### Model Buyer
	Script Path: .../model_buyer/virtualenv/bin/gunicorn
	Parameters: -b "0.0.0.0:9090" wsgi:app --preload
	Working directory: ../model_buyer


### Federated Trainer
	Script Path: .../federated_trainer/virtualenv/bin/gunicorn
	Parameters: -b "0.0.0.0:8080" wsgi:app --preload
	Working directory: ../federated_trainer


### Data Owner
	Script Path: .../data_owner/virtualenv/bin/gunicorn
	Parameters: -b "0.0.0.0:5000" wsgi:app --preload
	Working directory: ../data_owner

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/DeltaML/federated-learning-poc/tags). 

## Authors

* **Fabrizio Graffe** - *Dev* - [GFibrizo](https://github.com/GFibrizo)
* **Agustin Rojas** - *Dev* - [agrojas](https://github.com/agrojas)

See also the list of [contributors](https://github.com/DeltaML/federated-learning-poc/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

