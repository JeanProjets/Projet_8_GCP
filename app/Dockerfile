FROM python:3.11-slim

WORKDIR /app

# On installe les requirements de l'application
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le code de l'application et la donnée (images de test)
COPY app/ app/
COPY data/ data/

# --- Configuration du port (Décommenter selon le Cloud choisi) ---

# Pour Google Cloud Run (ou local standard) :
# EXPOSE 8501
# CMD ["streamlit", "run", "app/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]

# Pour Hugging Face Spaces (Port 7860 par défaut) :
EXPOSE 7860
CMD ["streamlit", "run", "app/app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]
