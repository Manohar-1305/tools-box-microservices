docker build -t text-to-audio-app:latest .
kind load docker-image text-to-audio-app:latest --name multi-node-cluster
