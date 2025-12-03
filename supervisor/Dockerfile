FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit port for supervisor dashboard
EXPOSE 8502

RUN mkdir -p ~/.streamlit
RUN echo "[server]\nheadless = true\nenableCORS = false\nport = 8502\n" > ~/.streamlit/config.toml

CMD ["streamlit", "run", "supervisor_dashboard.py", "--server.address=0.0.0.0", "--server.port=8502"]
