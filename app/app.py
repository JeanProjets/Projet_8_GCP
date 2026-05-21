import streamlit as st
import requests
import glob
import os
from PIL import Image
import base64
import io

# --- 1. Configuration UI ---
st.set_page_config(page_title="Future Vision Transport - Démos", layout="wide", page_icon="")

st.title("Segmentation Sémantique Embarquée")
st.markdown("Interface d'Inférence interagissant en direct avec l'API FastAPI construite lors de la Phase 5.")

# Cible du Microservice API
# --- Configuration du port local (Décommenter selon le Cloud choisi) ---
# Si tu testes pour GCP (Port 8000) :
# API_URL = os.getenv("API_URL", "http://localhost:8000")
# Si tu testes pour Hugging Face (Port 7860) :
API_URL = os.getenv("API_URL", "http://localhost:7860")

# --- 2. Fonctions Méthodologiques ---
@st.cache_data
def load_available_images():
    """ 
    Scanne intelligemment le dossier de Test pour remonter toute la flotte d'images réelles (Phase 6.1).
    Utilise le cache de Streamlit pour ne pas faire mouliner le disque dur à chaque clic !
    """
    img_dir = "data/P8_Cityscapes_leftImg8bit_trainvaltest/leftImg8bit/test/"
    if not os.path.exists(img_dir):
        return []
        
    image_paths = sorted(glob.glob(os.path.join(img_dir, "**/*_leftImg8bit.png"), recursive=True))
    return image_paths

images_list = load_available_images()

if not images_list:
    st.error("**Stop !** Dossier des images introuvable. J'ai cherché dans `data/P8_Cityscapes_leftImg8bit_trainvaltest`. Êtes-vous sûr d'avoir lancé `streamlit run app/app.py` depuis la racine de `Projet_8` ?")
    st.stop()

# --- 3. Barre de Menu (Sidebar) ---
st.sidebar.header("Tableau de Bord")
st.sidebar.markdown("Sélectionnez l'image issue des caméras embarquées pour la transmettre au réseau de neurones.")

# On allège visuellement la liste déroulante en n'affichant que le nom du fichier
images_names = [os.path.basename(p) for p in images_list]
selected_filename = st.sidebar.selectbox("Fichier à analyser :", images_names)
selected_path = images_list[images_names.index(selected_filename)]

# Algorithme pour reconstruire le chemin du "Ground Truth Color" (Masque Parfait) de Cityscapes
city_name = selected_filename.split('_')[0]
gt_color_filename = selected_filename.replace('_leftImg8bit.png', '_gtFine_color.png')
gt_color_path = os.path.join("data/P8_Cityscapes_gtFine_trainvaltest/gtFine/test/", city_name, gt_color_filename)

# --- 4. Le Client REST ---
if st.sidebar.button("Lancer l'Inférence de l'API"):
    st.markdown("---")
    
    with st.spinner("Transmission sécurisée à l'API FastAPI en cours..."):
        try:
            # Sérialisation : On capture l'image en données binaires pour le flux HTTP sortant
            with open(selected_path, "rb") as image_file:
                # payload 'multipart/form-data'
                files = {"file": (selected_filename, image_file, "image/png")}
                response = requests.post(f"{API_URL}/segmentation", files=files)
            
            # Si le serveur nous envoie un Code HTTP 200 (Succès Total)
            if response.status_code == 200:
                # L'API nous renvoie désormais directement l'image au format PNG ! (StreamingResponse)
                predicted_mask = Image.open(io.BytesIO(response.content))
                
                st.success("Triangulation serveur réussie ! Prédiction récupérée depuis l'API.")
                
                # --- VISUALISATION DES 3 COMPOSANTES (Phase 6.1 Guideline) ---
                col1, col2, col3 = st.columns(3)
                
                # A. La Réalité Capturée
                col1.subheader("Caméra (leftImg8bit)")
                col1.image(Image.open(selected_path), use_container_width=True)
                
                # B. Le Masque Parfait fourni par Cityscapes
                col2.subheader("Masque Vérité (Attendu)")
                if os.path.exists(gt_color_path):
                    col2.image(Image.open(gt_color_path), use_container_width=True)
                else:
                    col2.warning("Non fourni (Normal pour le Test-Set de compétition).")
                    
                # C. L'Intelligence Artificielle en Action
                col3.subheader("Prédiction FastAPI (Notre IA)")
                col3.image(predicted_mask, use_container_width=True)
                
                # Affichage des classes (Codées en dur ici car l'API renvoie directement une image pour optimiser)
                CLASSES = ['void', 'flat', 'construction', 'object', 'nature', 'sky', 'human', 'vehicle']
                with st.expander("Consulter la palette de couleurs sémantiques "):
                    st.write(", ".join(CLASSES))
                    
            else:
                st.error(f"Erreur Serveur (HTTP {response.status_code}) : Vous devez vérifier ce que l'API imprime dans son propre terminal.")
                
        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR CRITIQUE : L'API est injoignable sur l'URL ciblée (`{API_URL}`).")
            # st.info("Si vous testez en local pour GCP, lancez le serveur FastAPI via : `cd api && uvicorn main:app --port 8000` et vérifiez l'API_URL.")
            st.info("Si vous testez en local pour Hugging Face, lancez le serveur FastAPI via : `cd api && uvicorn main:app --port 7860` et vérifiez l'API_URL.")
