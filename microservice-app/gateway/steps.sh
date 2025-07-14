docker build -t microservice-gateway:latest .
kind load docker-image microservice-gateway:latest --name multi-node-cluster
kubectl apply -f gateway.yaml
http://localhost:30000


kind load docker-image microservice-gateway:latest --name multi-node-cluster
