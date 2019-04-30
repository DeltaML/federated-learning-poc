# DeltaML/federated-learning-poc

Repository that contains a Proof of Concept for the implementation of a Federated Learning framework.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites


[python3](https://www.python.org/download/releases/3.0/)


### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
git clone git@github.com:DeltaML/federated-learning-poc.git
cd federated-learning-poc/
python3 -m venv venv
source venvenv/bin/activate
pip install -r requirements.txt
```

## Running the tests

Run thes using
```
notests test
```

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

Run and scale clients
```
docker-compose up --scale cte_client=<N_CLIENTS>
```

## Using Pycharm

### Consumer
	Script Path: .../consumer/virtualenv/bin/gunicorn
	Parameters: -b "0.0.0.0:9090" wsgi:app --preload
	Working directory: ../consumer


### Server
	Script Path: .../server/virtualenv/bin/gunicorn
	Parameters: -b "0.0.0.0:8080" wsgi:app --preload
	Working directory: ../server


### Client
	Script Path: .../client/virtualenv/bin/gunicorn
	Parameters: -b "0.0.0.0:5000" wsgi:app --preload
	Working directory: ../client

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/DeltaML/federated-learning-poc/tags). 

## Authors

* **Fabrizio Graffe** - *Dev* - [GFibrizo](https://github.com/GFibrizo)
* **Agustin Rojas** - *Dev* - [agrojas](https://github.com/agrojas)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

