# Federated learning consumer

### Run consumer
gunicorn -b "0.0.0.0:9090" --chdir consumer/ wsgi:app --preload


### Execute prediction
curl -v -H "Content-Type: application/json" -X POST "http://localhost:9090/predict"