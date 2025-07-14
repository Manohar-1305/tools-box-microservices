docker build -t text-to-audio-app:latest .
kind load docker-image text-to-audio-app:latest --name multi-node-cluster
kubectl apply -f audio_deployment.yaml
kubectl get pods
kubectl get svc audio-service
