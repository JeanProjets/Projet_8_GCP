import os
import io
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image
import numpy as np

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Note : Le code pour Azure Log Analytics peut être configuré ici
# en utilisant azure-monitor-opentelemetry (si la clé de connexion est fournie via env)
# try:
#     from azure.monitor.opentelemetry import configure_azure_monitor
#     if "APPLICATIONINSIGHTS_CONNECTION_STRING" in os.environ:
#         configure_azure_monitor()
# except ImportError:
#     pass

CLASSES = ['void', 'flat', 'construction', 'object', 'nature', 'sky', 'human', 'vehicle']
COLORS = [
    [0, 0, 0], [128, 64, 128], [70, 70, 70], [153, 153, 153],
    [107, 142, 35], [70, 130, 180], [220, 20, 60], [0, 0, 142]
]

# Variables globales pour l'état de l'application
model = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/best_unet_model.keras')

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if os.path.exists(MODEL_PATH):
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            import tensorflow as tf
            logger.info("⏳ Chargement du modèle Keras...")
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            logger.info("✅ Modèle chargé avec succès !")
        except Exception as e:
            model = None
            logger.error(f"❌ Erreur critique de TensorFlow : {e}")
    else:
        logger.warning(f"⚠️ Modèle introuvable ({MODEL_PATH}). L'API tourne en 'MOCK MODE'.")
    yield
    # Nettoyage si nécessaire
    model = None

app = FastAPI(
    title="Cityscapes Segmentation API",
    description="API de segmentation sémantique pour Future Vision Transport",
    version="1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Service back-end de prédiction Actif."}

@app.get("/health")
def health_check():
    return {"status": "ok", "model_active": model is not None}

@app.post("/segmentation")
async def segmentation(file: UploadFile = File(...)):
    # Lire l'image envoyée
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    IMG_HEIGHT, IMG_WIDTH = 256, 512
    img_resized = image.resize((IMG_WIDTH, IMG_HEIGHT))

    if model is not None:
        # Prétraitement de l'image
        img_array = np.array(img_resized) / 255.0
        img_batch = np.expand_dims(img_array, axis=0)
        
        # Prédiction
        prediction = model.predict(img_batch, verbose=0)[0]
        mask_classes = np.argmax(prediction, axis=-1).astype(np.uint8)
    else:
        # Mock Mode : générer un masque vide si aucun modèle n'est chargé
        mask_classes = np.zeros((IMG_HEIGHT, IMG_WIDTH), dtype=np.uint8)

    # Colorisation du masque
    mask_colored = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), dtype=np.uint8)
    for class_id, color in enumerate(COLORS):
        mask_colored[mask_classes == class_id] = color

    mask_img = Image.fromarray(mask_colored)
    
    # Convertir l'image en bytes pour la réponse
    img_io = io.BytesIO()
    mask_img.save(img_io, format="PNG")
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")