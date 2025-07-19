docker build -t microservice-gateway:latest .
kind load docker-image microservice-gateway:latest --name multi-node-cluster
kubectl apply -f gateway.yaml
http://localhost:30000



docker build -t microservice-gateway:latest .
docker build -t text-to-audio-app:latest .
docker network create microservices-net

docker run -d \
  --name audio-service \
  --network microservices-net \
  -p 5003:5003 \
  text-to-audio-app:latest
  
docker run -d \
  --name gateway \
  --network microservices-net \
  -p 5000:5000 \
  -e AUDIO_SERVICE_URL=http://audio-service:5003 \
  microservice-gateway:latest

docker stop gateway audioservice
docker rm gateway audioservice
docker network create mynetwork

docker run -d \
  --name audioservice \
  --network mynetwork \
  -p 5003:5003 \
  text-to-audio-app

docker run -d \
  --name gateway \
  --network mynetwork \
  -p 5000:5000 \
  microservice-gateway

  docker exec -it gateway curl http://audioservice:5003/convert


