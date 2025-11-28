# Dockerfile for frontend
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Streamlit port
EXPOSE 8501

RUN mkdir -p ~/.streamlit
RUN echo "[server]\nheadless = true\nenableCORS = false\nport = 8501\n" > ~/.streamlit/config.toml


# Run Streamlit on 0.0.0.0 (all interfaces) for Kubernetes
CMD ["streamlit", "run", "client_dashboard.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
