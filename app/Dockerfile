FROM python:3.11-slim

WORKDIR /app

# On installe les requirements de l'application
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le code de l'application et la donnée (images de test)
COPY app/ app/
COPY data/ data/

# Port par défaut sur Hugging Face Spaces
EXPOSE 7860

# Lancement de Streamlit
CMD ["streamlit", "run", "app/app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]
