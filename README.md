# DeltaML/federated-learning-poc

[![Build Status](https://travis-ci.com/DeltaML/federated-learning-poc.svg?branch=master)](https://travis-ci.com/DeltaML/federated-learning-poc)
[![Coverage Status](https://coveralls.io/repos/github/DeltaML/federated-learning-poc/badge.svg?branch=master)](https://coveralls.io/github/DeltaML/federated-learning-poc?branch=master)

Repository that contains a Proof of Concept for the implementation of a Federated Learning framework.

## IMPORTANT:
**The code found in this repository was divided and moved into several repositories** one for each component of a platform that uses Federated Learning to train models preserving the privacy, Homomorphic Encryption to secure the model and Smart Contracts to pay each participant in the platform for the job done without having to trust in a third party.
An explanation of the whole project can be found in:
- [https://github.com/DeltaML/report](https://github.com/DeltaML/report) (currently only in spanish).

**The current repositories are:**
- **Model Buyer:**
  - API: [https://github.com/DeltaML/model-buyer](https://github.com/DeltaML/model-buyer)
  - UI: [https://github.com/DeltaML/model-buyer-ui](https://github.com/DeltaML/model-buyer-ui)
- **Data Owner:**
  - API: [https://github.com/DeltaML/data-owner](https://github.com/DeltaML/data-owner)
  - UI: [https://github.com/DeltaML/data-owner-ui](https://github.com/DeltaML/data-owner-ui)
- **Federated Aggregator:**
  - API:[https://github.com/DeltaML/federated-aggregator](https://github.com/DeltaML/federated-aggregator)
- **Smart Contract:**
  - [https://github.com/DeltaML/contract](https://github.com/DeltaML/contract)


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

