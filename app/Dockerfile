FROM python:3.11-slim

WORKDIR /app

# On installe les requirements de l'application
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le code de l'application et la donnée (images de test)
COPY app/ app/
COPY data/ data/

# Port utilisé par Streamlit
EXPOSE 8501

# Lancement de Streamlit
CMD ["streamlit", "run", "app/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
