# Guide Complet — Projet 8 : Déploiement d'un Modèle de Segmentation d'Images

> **Contexte** : Tu es ingénieur IA chez *Future Vision Transport*. Tu conçois le module de **segmentation d'images** dans une chaîne de vision embarquée pour véhicules autonomes. Le dataset est **Cityscapes**, le framework imposé est **Keras**, et tu dois livrer un modèle + API + application web déployés sur le Cloud.

---

## Phase 0 — Mise en place de l'environnement

### 0.1 Créer un environnement virtuel Python dédié
```bash
python -m venv venv_projet8
source venv_projet8/bin/activate
pip install tensorflow keras numpy pandas matplotlib opencv-python albumentations flask fastapi uvicorn streamlit
```
- **Why** : Isoler les dépendances évite les conflits entre projets. C'est une pratique professionnelle standard.
- **Notions** : *virtual environments*, gestion de dépendances avec `pip`, `requirements.txt`.

### 0.2 Structurer le répertoire de travail
```
Projet_8/
├── data/               # Données Cityscapes (déjà présent)
├── notebooks/          # Notebooks d'exploration et d'entraînement
├── src/                # Code source réutilisable (data generator, model, utils)
├── api/                # Code de l'API Flask/FastAPI
├── app/                # Code de l'application web Streamlit/Flask
├── models/             # Modèles sauvegardés (.h5, .keras)
├── docs/               # Note technique + supports de présentation
└── requirements.txt
```
- **Why** : Une structure claire rend le projet "industrialisable" (critère évalué dans les livrables) et facilite la collaboration.
- **Notions** : *project scaffolding*, bonnes pratiques d'organisation de projets ML.

### 0.3 Initialiser un dépôt Git
```bash
git init
echo "venv_projet8/\ndata/\nmodels/*.h5\n__pycache__/" > .gitignore
```
- **Why** : Le versionnement est indispensable pour tracer l'évolution du code, revenir en arrière, et montrer ta démarche.
- **Notions** : *Git*, versionnement, `.gitignore`.

---

## Phase 1 — Comprendre les données Cityscapes

### 1.1 Télécharger le jeu de données complet
> **Observation** : Ton dossier [data/](file:///Users/j/Documents/OC_Inge_IA/Projet_8/data) contient actuellement uniquement les **annotations gtFine** (masks de segmentation), pas les images brutes. Tu dois télécharger les images `leftImg8bit` depuis [cityscapes-dataset.com](https://www.cityscapes-dataset.com/).

- **Why** : Ton modèle prend en entrée les **images caméra** (leftImg8bit) et doit prédire les **masks de segmentation** (gtFine). Sans les images, tu ne peux pas entraîner.
- **Notions** : *supervised learning*, notion d'images d'entrée vs. ground truth / labels.

### 1.2 Comprendre la structure des fichiers
Pour chaque image, Cityscapes fournit :

| Fichier | Description |
|---------|-------------|
| `*_leftImg8bit.png` | Image caméra brute (1024×2048) |
| `*_gtFine_labelIds.png` | Mask avec label ID par pixel (0-33) |
| `*_gtFine_color.png` | Mask coloré (visualisation) |
| `*_gtFine_instanceIds.png` | Mask d'instances |
| `*_gtFine_polygons.json` | Annotations polygonales |

- **Why** : Comprendre ce que chaque fichier représente est crucial avant de construire ton pipeline de données. Tu utiliseras principalement `leftImg8bit` + `labelIds`.
- **Notions** : *semantic segmentation*, *instance segmentation*, label maps, correspondance pixel-classe.

### 1.3 Comprendre les 8 catégories principales vs les 32 sous-catégories

Le projet demande de travailler avec les **8 catégories principales** :

| ID Cat. | Catégorie | Sous-catégories incluses |
|---------|-----------|-------------------------|
| 0 | **void** | unlabeled, ego vehicle, rectification border, out of roi, static, dynamic |
| 1 | **flat** | road, sidewalk, parking, rail track |
| 2 | **construction** | building, wall, fence, guard rail, bridge, tunnel |
| 3 | **object** | pole, polegroup, traffic light, traffic sign |
| 4 | **nature** | vegetation, terrain |
| 5 | **sky** | sky |
| 6 | **human** | person, rider |
| 7 | **vehicle** | car, truck, bus, caravan, trailer, train, motorcycle, bicycle |

- **Why** : C'est une contrainte explicite du projet (Franck). Tu dois mapper les 32 sous-catégories vers ces 8. Cela simplifie le problème et rend le modèle plus robuste.
- **Notions** : *label remapping*, *category grouping*, dictionnaire de correspondance Cityscapes.

### 1.4 Explorer visuellement les données (EDA)
Dans un notebook, afficher côte à côte :
- L'image brute
- Le mask coloré (`gtFine_color`)
- Le mask labelIds remappé vers les 8 catégories
- Distribution des classes par image (histogrammes)

- **Why** : L'EDA permet de détecter le *class imbalance* (par exemple, "road" et "building" dominent, "rider" est rare). Cela guidera tes choix d'augmentation de données et de loss function.
- **Notions** : *Exploratory Data Analysis*, *class imbalance*, visualisation de masks de segmentation, `matplotlib.imshow()`.

---

## Phase 2 — État de l'Art et Recherche Bibliographique

### 2.1 Étudier les architectures de segmentation sémantique

Architectures incontournables à comprendre et comparer :

| Architecture | Principe clé | Avantage |
|-------------|--------------|----------|
| **FCN** (Fully Convolutional Network) | Remplace les couches FC par des convolutions | Premier modèle end-to-end pour la segmentation |
| **U-Net** | Encoder-decoder avec skip connections | Excellent pour les détails fins, idéal pour les données limitées |
| **SegNet** | Encoder-decoder avec pooling indices | Plus léger en mémoire que U-Net |
| **DeepLab v3+** | Atrous convolutions + ASPP + encoder-decoder | State-of-the-art, capture multi-échelle |
| **PSPNet** | Pyramid Pooling Module | Capture le contexte global |

- **Why** : La note technique demande une "présentation des différentes approches et une synthèse de l'état de l'art". Tu dois comprendre les forces/faiblesses de chaque architecture pour justifier ton choix.
- **Notions** : *encoder-decoder architecture*, *skip connections*, *atrous/dilated convolutions*, *feature pyramid*, *receptive field*.

### 2.2 Étudier les métriques de segmentation

| Métrique | Formule/Description |
|----------|-------------------|
| **Pixel Accuracy** | % de pixels correctement classifiés |
| **Mean IoU (mIoU)** | Intersection over Union moyenné sur toutes les classes |
| **Dice Coefficient** | 2×TP / (2×TP + FP + FN) |
| **Per-class IoU** | IoU calculé pour chaque classe individuellement |

- **Why** : Le pixel accuracy est trompeur sur des données déséquilibrées. Le mIoU est la métrique standard en segmentation sémantique et sera celle que l'évaluateur attend.
- **Notions** : *IoU (Intersection over Union)*, *Dice score*, *confusion matrix* pixel-level, *mean IoU*.

### 2.3 Étudier les loss functions adaptées

- **Categorical Cross-Entropy** : Standard, mais sensible au class imbalance
- **Weighted Cross-Entropy** : Pondération inversement proportionnelle à la fréquence de la classe
- **Dice Loss** : Optimise directement le Dice Coefficient
- **Focal Loss** : Réduit la contribution des exemples bien classifiés
- **Combinaison** : Dice Loss + Cross-Entropy souvent utilisée en pratique

- **Why** : Le choix de la loss function a un impact direct sur les performances, surtout avec des classes déséquilibrées (road vs rider).
- **Notions** : *loss functions*, *class weighting*, *focal loss*, *dice loss*.

---

## Phase 3 — Pipeline de Données

### 3.1 Créer un Data Generator Keras

```python
class CityscapesGenerator(tf.keras.utils.Sequence):
    def __init__(self, image_paths, mask_paths, batch_size, img_size, augment=False):
        ...
    def __getitem__(self, idx):
        # Charge batch d'images + masks
        # Remapping 32 → 8 catégories
        # Resize
        # Augmentation (si train)
        # One-hot encoding du mask
        ...
```

- **Why** : Les images Cityscapes (1024×2048) sont trop volumineuses pour tout charger en RAM. Un generator charge les données par batch à la volée. C'est un critère du livrable ("caractère industrialisable").
- **Notions** : `tf.keras.utils.Sequence`, *batch loading*, *lazy loading*, *one-hot encoding* de masks, *yield* vs *return*.

### 3.2 Implémenter le label remapping (32 → 8 catégories)

```python
# Dictionnaire de mapping utilisant la documentation Cityscapes
LABEL_TO_CATEGORY = {
    0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,   # void
    7: 1, 8: 1, 9: 1, 10: 1,                       # flat
    11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2,      # construction
    17: 3, 18: 3, 19: 3, 20: 3,                     # object
    21: 4, 22: 4,                                    # nature
    23: 5,                                           # sky
    24: 6, 25: 6,                                    # human
    26: 7, 27: 7, 28: 7, 29: 7, 30: 7, 31: 7, 32: 7, 33: 7  # vehicle
}
```

- **Why** : Franck (le collègue en charge du traitement d'images) a spécifié que seules les 8 catégories principales sont nécessaires. Ce remapping doit être fait dans le pipeline de données, pas manuellement.
- **Notions** : *label encoding*, *numpy vectorized mapping* (`np.vectorize` ou table de lookup), correspondance Cityscapes.

### 3.3 Implémenter l'augmentation de données

Techniques à appliquer :
- **Flip horizontal** (le plus commun pour la conduite)
- **Rotation légère** (±10°)
- **Variations de luminosité/contraste**
- **Random crop + resize**
- **Ajout de bruit gaussien**

> L'augmentation doit être appliquée **identiquement** à l'image ET au mask !

- **Why** : Le livrable demande explicitement des "gains obtenus avec les approches d'augmentation des données". L'augmentation permet de régulariser le modèle et d'augmenter virtuellement la taille du dataset.
- **Notions** : *data augmentation*, bibliothèque `albumentations` (applique les mêmes transformations géométriques à l'image et au mask), *overfitting prevention*.

### 3.4 Gérer le redimensionnement des images

Réduire les images de 1024×2048 à une taille gérable :
- **256×512** : bon compromis vitesse/qualité pour les premiers tests
- **512×1024** : meilleure résolution si ressources GPU suffisantes

- **Why** : Les images originales sont très grandes. Entraîner en pleine résolution nécessite un GPU puissant (32+ Go VRAM). Le redimensionnement est un compromis nécessaire.
- **Notions** : *image resizing*, interpolation bilinéaire vs nearest-neighbor (pour les masks !), *aspect ratio preservation*.

---

## Phase 4 — Entraînement du Modèle

### 4.1 Commencer avec un modèle simple (baseline)

Entraîner un U-Net simple depuis zéro comme baseline :
- Encoder : blocs Conv2D + BatchNorm + ReLU + MaxPool
- Decoder : UpSampling2D + Concatenate (skip connections) + Conv2D
- Sortie : Conv2D(8, (1,1), activation='softmax')

- **Why** : Un modèle simple permet de valider que tout le pipeline fonctionne (data loading, training loop, évaluation) avant d'investir du temps dans des architectures plus complexes.
- **Notions** : *U-Net architecture*, *encoder-decoder*, *skip connections*, *softmax pour classification multi-classe pixel-level*.

### 4.2 Utiliser le Transfer Learning

Utiliser un backbone pré-entraîné sur ImageNet :
- **MobileNetV2** : léger, idéal pour l'embarqué
- **ResNet50** : bon compromis performance/poids
- **EfficientNet** : état de l'art en efficacité

```python
base_model = tf.keras.applications.MobileNetV2(input_shape=(256, 512, 3), include_top=False, weights='imagenet')
```

- **Why** : Le transfer learning permet d'obtenir de bien meilleures performances avec moins de données et moins de temps d'entraînement. Les features bas-niveau (contours, textures) apprises sur ImageNet sont transférables.
- **Notions** : *transfer learning*, *feature extraction vs fine-tuning*, *backbone freezing/unfreezing*, `keras.applications`.

### 4.3 Implémenter un modèle avancé (DeepLab v3+ ou similaire)

Options :
- Utiliser `segmentation_models` library : `pip install segmentation-models`
- Implémenter DeepLab v3+ manuellement avec Keras
- Utiliser TensorFlow Hub pour charger un modèle pré-entraîné

- **Why** : La comparaison entre un modèle simple (baseline) et un modèle avancé est attendue dans la note technique. DeepLab v3+ est souvent le meilleur choix pour Cityscapes.
- **Notions** : *ASPP (Atrous Spatial Pyramid Pooling)*, *dilated convolutions*, *multi-scale feature extraction*.

### 4.4 Configurer l'entraînement

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',  # ou dice_loss + CE combinée
    metrics=['accuracy', MeanIoU(num_classes=8)]
)

callbacks = [
    tf.keras.callbacks.ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_mean_iou', mode='max'),
    tf.keras.callbacks.EarlyStopping(patience=10, monitor='val_mean_iou', mode='max'),
    tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5),
    tf.keras.callbacks.TensorBoard(log_dir='./logs')
]
```

- **Why** : Les callbacks automatisent la sauvegarde du meilleur modèle, l'arrêt précoce (évite l'overfitting), et l'ajustement du learning rate. C'est une démarche professionnelle.
- **Notions** : *callbacks Keras*, *early stopping*, *learning rate scheduling*, *model checkpointing*, *TensorBoard*.

### 4.5 Entraîner et comparer les modèles

Pour chaque modèle, documenter :
- Architecture utilisée
- Hyperparamètres (lr, batch size, epochs, augmentation)
- Courbes train/val loss et mIoU
- Per-class IoU sur le validation set
- Prédictions visuelles (image / ground truth / prédiction)

- **Why** : La soutenance demande la "comparaison des modèles" (10 min dédiées). Tu dois montrer une démarche itérative et justifier le modèle final retenu.
- **Notions** : *hyperparameter tuning*, *learning curves analysis*, *overfitting vs underfitting diagnosis*, *model selection*.

### 4.6 Évaluer sur le jeu de test

Calculer les métriques finales sur le test set (Berlin, Bielefeld, Bonn, Leverkusen, Mainz, Munich) :
- mIoU global
- IoU par classe
- Matrice de confusion pixel-level
- Visualisations qualitatives

- **Why** : L'évaluation sur le test set (jamais vu pendant l'entraînement) donne une estimation non biaisée des performances. C'est la norme en ML.
- **Notions** : *train/val/test split*, *generalization*, *qualitative vs quantitative evaluation*.

---

## Phase 5 — Développement de l'API de Prédiction

### 5.1 Choisir entre Flask et FastAPI

| Critère | Flask | FastAPI |
|---------|-------|---------|
| Facilité | Plus simple | Async concepts |
| Performance | Synchrone | Asynchrone natif |
| Documentation auto | | Swagger/OpenAPI inclus |
| Typing | | Pydantic intégré |

> **Recommandation** : FastAPI — la doc auto est un vrai plus pour Laura et la soutenance.

- **Why** : Laura veut une "API simple à utiliser". FastAPI génère automatiquement une documentation interactive (Swagger UI) qui permet de tester l'API sans code client.
- **Notions** : *REST API*, *endpoints*, *HTTP methods* (POST), *content types* (multipart/form-data, JSON).

### 5.2 Concevoir l'endpoint de prédiction

```python
from fastapi import FastAPI, File, UploadFile
import numpy as np
from PIL import Image
import io

app = FastAPI(title="Cityscapes Segmentation API")

# Charger le modèle au démarrage
model = tf.keras.models.load_model('best_model.keras')

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Lire l'image uploadée
    image = Image.open(io.BytesIO(await file.read()))
    # 2. Prétraiter (resize, normalisation)
    # 3. Prédire le mask
    # 4. Post-traiter (argmax, resize au format original)
    # 5. Retourner le mask (encodé en base64 ou en JSON)
    return {"mask": mask_as_list, "classes": class_names}
```

- **Why** : Cet endpoint est le cœur du livrable 2. Il prend une image et retourne le mask prédit. Il sera consommé par l'application web (livrable 3).
- **Notions** : *API endpoint design*, *image I/O* (bytes → PIL → numpy), *model inference pipeline*, *base64 encoding*.

### 5.3 Ajouter des endpoints utilitaires

- `GET /` : Infos sur l'API (version, modèle utilisé, classes)
- `GET /health` : Health check
- `GET /classes` : Liste des 8 catégories et leurs couleurs

- **Why** : Des endpoints d'information facilitent l'intégration et le monitoring. C'est une bonne pratique d'architecture API.
- **Notions** : *API design patterns*, *health checks*, *API versioning*.

### 5.4 Tester l'API en local

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
# Tester sur http://localhost:8000/docs (Swagger UI)
```

- **Why** : Toujours tester en local avant de déployer. La Swagger UI permet de tester visuellement l'upload d'image et la réponse.
- **Notions** : *local development server*, *API testing*, *Swagger/OpenAPI*.

---

## Phase 6 — Développement de l'Application Web

### 6.1 Concevoir l'application Streamlit (ou Flask)

L'application doit permettre :
1. **Afficher la liste des IDs** des images disponibles (test set)
2. **Sélectionner un ID** → lancer la prédiction via l'API
3. **Afficher 3 images côte à côte** : image réelle | mask réel | mask prédit

```python
import streamlit as st
import requests

st.title("Segmentation d'Images - Future Vision Transport")

# Liste des images disponibles
image_ids = get_available_image_ids()
selected_id = st.selectbox("Sélectionner une image :", image_ids)

if st.button("Lancer la prédiction"):
    # Appel à l'API
    response = requests.post(API_URL + "/predict", files={"file": image_bytes})
    predicted_mask = decode_response(response.json())
    
    col1, col2, col3 = st.columns(3)
    col1.image(original_image, caption="Image réelle")
    col2.image(ground_truth_mask, caption="Mask réel")
    col3.image(predicted_mask, caption="Mask prédit")
```

- **Why** : Cette application est l'interface de démonstration (livrable 3). Elle doit consommer l'API, pas faire la prédiction directement — cela prouve que l'architecture est bien découplée.
- **Notions** : *Streamlit*, *API consumption* (`requests`), *image display*, *UI/UX pour une démo*, *client-server architecture*.

### 6.2 Ajouter des fonctionnalités bonus

- Palette de couleurs pour les classes (légende)
- Overlay du mask sur l'image originale (transparence)
- Métriques affichées (IoU par classe vs ground truth)
- Upload d'une image personnelle (pas du dataset)

- **Why** : Ces fonctionnalités impressionnent l'évaluateur et montrent une maîtrise au-delà du minimum requis.
- **Notions** : *image compositing*, *alpha blending*, *color mapping*.

---

## Phase 7 — Déploiement sur le Cloud

### 7.1 Choisir une plateforme Cloud

| Plateforme | Coût | Difficulté | GPU |
|-----------|------|-----------|-----|
| **Render** | Gratuit (limité) | ⭐⭐ | |
| **Railway** | Gratuit ($5 crédit) | ⭐⭐ | |
| **Azure Web App** | Free tier disponible | ⭐⭐⭐ | Option payante |
| **Google Cloud Run** | Free tier généreux | ⭐⭐⭐ | |
| **PythonAnywhere** | Gratuit (très limité) | ⭐ | |
| **AWS (EC2/Lambda)** | Free tier 12 mois | ⭐⭐⭐⭐ | Option payante |

- **Why** : Le déploiement Cloud est obligatoire pour la soutenance. Tu dois faire une démo en live et l'enregistrer. Choisis en fonction de ton budget et de ta familiarité.
- **Notions** : *cloud deployment*, *PaaS vs IaaS*, *containerization concepts*.

### 7.2 Containeriser avec Docker

```dockerfile
# API
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- **Why** : Docker garantit que l'environnement est identique en local et en production. La plupart des plateformes Cloud supportent Docker nativement.
- **Notions** : *Docker*, *Dockerfile*, *containers vs VMs*, *image build*, *port mapping*.

### 7.3 Déployer l'API et l'application

Deux déploiements séparés :
1. **API** : déploiement du service de prédiction
2. **App web** : déploiement de l'interface Streamlit (pointe vers l'URL de l'API)

- **Why** : Séparer l'API de l'application web est une architecture microservices. Cela prouve la modularité de ton système.
- **Notions** : *microservices architecture*, *environment variables* pour l'URL de l'API, *CORS configuration*.

### 7.4 Enregistrer la démo pendant la soutenance

> **Important** : Le sujet précise que l'évaluateur et l'étudiant doivent **enregistrer la démo** pendant la soutenance pour que le jury puisse la visionner. Tu pourras ensuite couper le service Cloud pour éviter les coûts.

- **Why** : C'est une exigence explicite du sujet. Prépare un outil d'enregistrement d'écran (OBS, QuickTime, etc.).
- **Notions** : *screen recording*, préparation de démo.

---

## Phase 8 — Rédaction de la Note Technique (~10 pages)

### 8.1 Structure recommandée

| Section | Contenu | ~Pages |
|---------|---------|--------|
| **1. Introduction** | Contexte (Future Vision Transport), objectifs, contraintes | 1 |
| **2. État de l'Art** | Revue des architectures (FCN, U-Net, SegNet, DeepLab), métriques | 2 |
| **3. Dataset et Préparation** | Cityscapes, 8 catégories, EDA, augmentation | 1.5 |
| **4. Modèle Retenu** | Architecture détaillée, hyperparamètres, justification du choix | 2 |
| **5. Résultats** | Comparaison des modèles, mIoU, courbes, gains de l'augmentation | 2 |
| **6. Mise en Production** | Architecture API + App, déploiement Cloud | 1 |
| **7. Conclusion** | Bilan, limites, pistes d'amélioration | 0.5 |

- **Why** : La note technique est un livrable clé (livrable 4). Elle doit démontrer ta rigueur scientifique et ta capacité à synthétiser.
- **Notions** : *technical writing*, *scientific methodology*, *results presentation*.

### 8.2 Points clés à inclure

- **Comparaison explicite** des modèles (tableau mIoU)
- **Gains de l'augmentation** : comparer modèle sans augmentation vs avec
- **Visualisations** : courbes de loss, exemples de prédictions, matrice de confusion
- **Pistes d'amélioration** : Real-time inference, quantization, pruning, TensorRT

- **Why** : Ces éléments sont explicitement demandés dans le descriptif des livrables.
- **Notions** : *ablation study*, *model comparison*, *scientific rigor*.

---

## Phase 9 — Support de Présentation (max 30 slides)

### 9.1 Structure calquée sur le timing de soutenance

| Bloc | Durée | Slides | Contenu |
|------|-------|--------|---------|
| **Contexte & Objectifs** | 5 min | 5-7 | Entreprise, chaîne de vision, ton rôle, métriques |
| **Modèles & Résultats** | 10 min | 12-15 | Architectures, comparaisons, visualisations, augmentation |
| **Mise en Production** | 5 min | 5-8 | Architecture API/App, déploiement, démo live |

- **Why** : La soutenance est strictement chronométrée (20 min ±5). Une présentation trop courte (<15 min) ou trop longue (>25 min) peut être refusée.
- **Notions** : *presentation skills*, *storytelling technique*, *demo preparation*.

### 9.2 Préparer la démo live

Préparer un script de démo :
1. Ouvrir l'application web déployée
2. Sélectionner une image du test set
3. Lancer la prédiction
4. Montrer image / mask réel / mask prédit côte à côte
5. Éventuellement tester avec une image uploadée

> Tester la démo **plusieurs fois avant** la soutenance !

- **Why** : La démo est le moment fort de la soutenance. Un bug en live est très pénalisant. Prépare aussi des screenshots de backup au cas où le Cloud tombe.
- **Notions** : *demo rehearsal*, *fallback plan*.

---

## Checklist des Livrables

| # | Livrable | Format | Nommage |
|---|----------|--------|---------|
| 1 | **Scripts/Notebooks** (pipeline complet) | `.ipynb` / `.py` | `Nom_Prénom_1_scripts_mmaaaa` |
| 2 | **API de prédiction** (déployée sur le Cloud) | Flask/FastAPI | `Nom_Prénom_2_API_mmaaaa` |
| 3 | **Application web** (déployée sur le Cloud) | Streamlit/Flask | `Nom_Prénom_3_application_Flask_mmaaaa` |
| 4 | **Note technique** (~10 pages) | PDF | `Nom_Prénom_4_note_technique_mmaaaa` |
| 5 | **Présentation** (max 30 slides) | PPTX/PDF | `Nom_Prénom_5_presentation_mmaaaa` |

> Tout doit être dans un **zip** nommé `Titre_du_projet_nom_prénom`.

---

## Notions Clés à Maîtriser (Résumé)

| Domaine | Notions |
|---------|---------|
| **Computer Vision** | Semantic segmentation, encoder-decoder, skip connections, dilated convolutions |
| **Deep Learning** | Transfer learning, data augmentation, loss functions (Dice, Focal, CE), callbacks |
| **Keras/TensorFlow** | `tf.keras.utils.Sequence`, `keras.applications`, custom training loops, `MeanIoU` |
| **MLOps** | Docker, API REST, déploiement Cloud, CI/CD basique |
| **Data Engineering** | Data generators, label remapping, preprocessing pipelines |
| **Évaluation** | mIoU, Dice, pixel accuracy, confusion matrix, per-class metrics |
| **Communication** | Note technique, présentation de résultats, démo live |
