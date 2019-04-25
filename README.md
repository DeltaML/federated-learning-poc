# federated-learning-poc
Repository that contains a Proof of Concept for the implementation of a Federated Learning framework.


# Run 
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