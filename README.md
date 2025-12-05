kubectl create secret generic ollama-secret \
  --from-literal=OLLAMA_USER=admin \
  --from-literal=OLLAMA_PASS=SuperSafe123 \
  --from-literal=OLLAMA_URL=https://your-ngrok-url.ngrok-free.app/api/generate
