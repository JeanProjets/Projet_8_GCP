# Déploiement sur Google Cloud Platform (GCP) avec Cloud Run

Félicitations pour le nettoyage du projet ! Nous avons désormais un dossier propre, prêt à être envoyé sur GCP.
Puisque le modèle `best_unet_model.keras` est lourd et que nous l'avons ajouté à `.gitignore`, il ne sera pas poussé sur GitHub. **La solution la plus simple est de déployer directement depuis ton Mac en utilisant le terminal**.

Google Cloud propose une commande magique : `gcloud run deploy --source .`. 
Cette commande va prendre tout ton dossier local (incluant le modèle .keras, grâce au `.gcloudignore`), l'envoyer de façon sécurisée à Google, construire le conteneur Docker dans le cloud, et le déployer.

Voici le guide étape par étape :

## Étape 1 : Prérequis sur Google Cloud
1. Va sur [Google Cloud Console](https://console.cloud.google.com/).
2. Crée un nouveau projet (ex: `projet-8-vision`).
3. Assure-toi que la **Facturation (Billing)** est activée pour ce projet.
4. Active l'API **Cloud Run** et **Cloud Build** via la barre de recherche en haut.

## Étape 2 : Installer le SDK Google Cloud sur ton Mac
Si tu ne l'as pas déjà fait, installe l'outil CLI de Google Cloud sur ton Mac :
1. Télécharge-le ou utilise Homebrew : `brew install --cask google-cloud-sdk`
2. Connecte-toi via le terminal :
   ```bash
   gcloud auth login
   ```
3. Sélectionne ton projet :
   ```bash
   gcloud config set project ID_DE_TON_PROJET
   ```

## Étape 3 : Déployer l'API FastAPI
L'API est le cœur du projet. Nous allons déployer le code qui se trouve dans le dossier `api/`.
Dans le terminal, à la racine du projet (`Projet_8_GCP`), tape cette commande :

```bash
gcloud run deploy p8-api \
  --source . \
  --allow-unauthenticated \
  --region europe-west9 \
  --memory 2Gi \
  --command "uvicorn,main:app,--host,0.0.0.0,--port,8000" \
  --set-env-vars="PORT=8000" \
  --working-dir="/app/api"
```

**Pourquoi ces options ?**
- `--source .` : Envoie tout le code (y compris le dossier `models/` et le gros fichier keras).
- `--memory 2Gi` : Donne 2 Go de RAM au conteneur pour pouvoir charger le réseau de neurones Keras sans crasher.
- `--working-dir="/app/api"` : Dit au conteneur Docker de se placer dans le bon dossier.

*Remarque : Quand la commande se termine, elle te fournira une URL de type `https://p8-api-xxx.run.app`. Garde-la précieusement !*

## Étape 4 : Déployer l'Application Streamlit
Maintenant que ton API tourne sur GCP, il faut dire à ton application Streamlit de communiquer avec elle.

1. Ouvre le fichier `app/app.py`.
2. Vérifie que la ligne de l'API utilise bien la variable d'environnement : `API_URL = os.getenv("API_URL", "http://localhost:8000")`.
3. Lance le déploiement de Streamlit avec la commande suivante (en remplaçant `URL_API_DE_L_ETAPE_3` par la vraie URL obtenue ci-dessus) :

```bash
gcloud run deploy p8-streamlit \
  --source . \
  --allow-unauthenticated \
  --region europe-west9 \
  --port 8501 \
  --command "streamlit,run,app/app.py,--server.port,8501,--server.address,0.0.0.0" \
  --set-env-vars="API_URL=URL_API_DE_L_ETAPE_3"
```

## Bonus : GitHub Actions (CI/CD)
Vu que le modèle n'est pas sur GitHub, un pipeline d'intégration continue "classique" (qui build à partir de GitHub seul) ne fonctionnera pas out-of-the-box sans héberger le modèle sur un Google Cloud Storage (Bucket). 
Pour une première mise en production simple et rapide, **la méthode `gcloud run deploy` depuis ton terminal est de loin la plus facile et recommandée**. 

C'est prêt ! Tu peux tester ton interface Streamlit avec l'URL publique générée.
