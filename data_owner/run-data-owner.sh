#!/usr/bin/env bash

./data_owner/ui/start_client.sh &

gunicorn -b 0.0.0.0:5000 wsgi:app --timeout 600 --chdir data_owner/ --preload
