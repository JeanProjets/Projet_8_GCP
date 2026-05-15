# Déploiement sur Hugging Face Spaces (100% Gratuit)

Hugging Face Spaces est la plateforme idéale pour héberger ce projet d'école gratuitement sans avoir besoin d'entrer une carte bancaire.
Étant donné que ton modèle principal `best_unet_model.keras` fait 23 Mo, il passe parfaitement sur GitHub et sur Hugging Face sans avoir besoin de configurations complexes (pas besoin de Git LFS).

Puisque nous avons conçu l'architecture en deux microservices distincts (API et Application Streamlit), nous allons créer **deux Spaces** sur Hugging Face.

## Étape 1 : Créer le Space pour l'API (FastAPI)

1. Connecte-toi sur [Hugging Face](https://huggingface.co/) et clique sur **"New Space"** en haut à droite.
2. Remplis les informations :
   - **Space name** : `projet-8-api` (par exemple).
   - **License** : MIT (ou laisse vide).
   - **Select the Space SDK** : Choisis **Docker** (puis "Blank" s'il te propose des sous-options).
   - **Space Hardware** : Laisse sur la version **Gratuite (Free)** (2 vCPU, 16GB RAM).
   - Clique sur **"Create Space"**.
3. Une fois créé, Hugging Face te propose d'ajouter des fichiers. L'idéal est de lier ton compte GitHub :
   - Rends-toi dans les **Settings** (Paramètres) de ton Space Hugging Face.
   - Cherche la section permettant de connecter ton dépôt GitHub (ou pousse simplement le code actuel sur l'URL Git que Hugging Face te fournit).
   - **IMPORTANT** : Dans la configuration du Space (ou dans le fichier README.md généré par HF au tout début de ton repo côté HF), ajoute ces métadonnées en haut de ton fichier :
     ```yaml
     ---
     title: Projet 8 API
     emoji: 🚀
     colorFrom: blue
     colorTo: indigo
     sdk: docker
     pinned: false
     app_port: 7860
     dockerfile: api/Dockerfile
     ---
     ```
     *L'option `dockerfile: api/Dockerfile` est magique : elle dit à Hugging Face de construire l'image avec ce fichier précis.*
4. Ton API va "Build" (se construire) puis "Run".
5. Une fois que c'est au vert (Running), **copie l'URL de ton API** (disponible via "App" -> clique droit "Inspect" ou via le menu "Embed this space"). Elle ressemblera à `https://ton-pseudo-projet-8-api.hf.space`.

## Étape 2 : Créer le Space pour l'App (Streamlit)

1. Crée un **deuxième "New Space"** sur Hugging Face.
2. Remplis les informations :
   - **Space name** : `projet-8-app`.
   - **Select the Space SDK** : Choisis **Docker** (pas Streamlit natif, car notre Dockerfile est configuré sur mesure).
3. Va dans les **Settings** de ce nouveau Space et cherche la section **"Variables and secrets"**.
   - Ajoute un **"New Secret"** ou une **"New Environment Variable"**.
   - Nom (Name) : `API_URL`
   - Valeur (Value) : L'URL de l'étape précédente (ex: `https://ton-pseudo-projet-8-api.hf.space`).
4. Connecte ton code GitHub (ou pousse-le) exactement comme à l'étape 1.
5. Dans le fichier `README.md` de ce deuxième Space côté Hugging Face, ajoute ces métadonnées :
     ```yaml
     ---
     title: Projet 8 Streamlit
     emoji: 🚗
     colorFrom: red
     colorTo: orange
     sdk: docker
     pinned: false
     app_port: 7860
     dockerfile: app/Dockerfile
     ---
     ```

## C'est fini ! 🎉
Hugging Face va construire ton Docker Streamlit. Une fois terminé, tu auras accès à ton interface Streamlit publique et elle communiquera avec ton API Hugging Face !

*Rappel : Si tu ne visites pas ton application pendant 48 heures, Hugging Face la mettra en pause pour économiser de l'énergie. Il suffira de retourner sur la page et de cliquer sur "Restart" pour la réveiller en 2 minutes.*
