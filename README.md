minikube start

kubectl create secret generic ollama-secret \
  --from-literal=OLLAMA_USER=admin \
  --from-literal=OLLAMA_PASS=SuperSafe123 \


--kubectl apply -f k8s/ollama-deployment.yaml\
--kubectl apply -f k8s/backend-deployment.yaml\
--kubectl apply -f k8s/frontend-deployment.yaml\
--kubectl apply -f k8s/supervisor-dashboard.yaml\
--kubectl apply -f k8s/backend-hpa.yaml\


minikube service frontend-service\
minikube service supervisor-service\
