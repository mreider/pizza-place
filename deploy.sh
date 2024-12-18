#kubectl apply -n pizza-shop -f otel-collector.yaml
kubectl apply -n pizza-shop -f k8s/redis-deployment.yaml
kubectl apply -n pizza-shop -f k8s/deployment.yaml