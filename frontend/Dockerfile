FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit streamlit-autorefresh requests

COPY . /app/

EXPOSE 8501

CMD ["streamlit", "run", "client_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
