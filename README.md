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