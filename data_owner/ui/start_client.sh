#!/bin/sh

gunicorn -b 0.0.0.0:5000 wsgi:app --timeout 600 --graceful-timeout 600 --preload
cd ui/
npm install
npm start
