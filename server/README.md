docker build -t federated-learning-server --rm .

docker run --rm -it -p 8080:5001 federated-learning-server
