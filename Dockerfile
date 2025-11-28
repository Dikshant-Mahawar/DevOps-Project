FROM ollama/ollama:latest

# Copy your Modelfile into the image
COPY ModelFile /ModelFile

# Expose Ollama API
EXPOSE 11434

# Start Ollama server and preload model when container runs
CMD ["sh", "-c", "ollama serve & sleep 5 && ollama create salon-llm -f /ModelFile && wait"]
