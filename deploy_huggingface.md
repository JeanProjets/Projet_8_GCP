# Déploiement Automatisé sur Hugging Face Spaces (100% Gratuit)

Hugging Face Spaces est la plateforme idéale pour héberger ce projet d'école gratuitement sans avoir besoin d'entrer une carte bancaire.
Étant donné que ton modèle principal `best_unet_model.keras` fait 23 Mo, il passe parfaitement sur GitHub.

Grâce à la nouvelle **GitHub Action** que nous avons mise en place (`.github/workflows/sync-to-hub.yml`), le déploiement est désormais **100% automatisé**. Dès que tu pousses du code sur la branche `main` de ton GitHub, l'action se charge de créer les bons fichiers `README.md` avec les bonnes métadonnées (le port `7860`, le bon `Dockerfile`) et d'envoyer le code à tes espaces Hugging Face.

Il te suffit de suivre ces étapes d'initialisation **une seule fois** :

## Étape 1 : Préparer tes Spaces sur Hugging Face

Pour que l'automatisation fonctionne, les conteneurs doivent exister sur ton compte Hugging Face.

1. Connecte-toi sur [Hugging Face](https://huggingface.co/) et clique sur **"New Space"** en haut à droite.
2. Crée le Space de l'API :
   - **Space name** : `projet-8-api` *(Attention : respecte exactement cette casse ou modifie le script Github Action).*
   - **Select the Space SDK** : Choisis **Docker** (puis "Blank" s'il te propose des sous-options).
   - **Space Hardware** : Laisse sur la version **Gratuite (Free)** (2 vCPU, 16GB RAM).
   - Clique sur **"Create Space"**.
3. Recommence l'opération pour créer le Space de l'Application :
   - **Space name** : `projet-8-app`
   - **Select the Space SDK** : Choisis **Docker** également.

## Étape 2 : Lier les deux espaces avec la variable d'environnement

Ton application Streamlit (`projet-8-app`) a besoin de savoir où se trouve ton API (`projet-8-api`) pour lui envoyer les images.

1. Va sur la page de ton Space **`projet-8-api`** et copie son URL publique (elle ressemble à `https://ton-pseudo-projet-8-api.hf.space`). Tu peux la trouver en cliquant sur "App" ou sur le bouton "Embed this space".
2. Va dans les **Settings** (Paramètres) de ton Space **`projet-8-app`**.
3. Cherche la section **"Variables and secrets"**.
4. Ajoute une **"New Environment Variable"** (ou "New Secret") :
   - Nom (Name) : `API_URL`
   - Valeur (Value) : L'URL que tu as copiée (ex: `https://ton-pseudo-projet-8-api.hf.space`).

## Étape 3 : Laisser la Magie GitHub Opérer !

Puisque tu as déjà configuré le secret `HF_TOKEN` dans ton GitHub, tout est prêt.

- Si le code est déjà sur ton GitHub, rends-toi sur la page de ton dépôt GitHub, dans l'onglet **"Actions"**.
- Tu devrais voir un workflow nommé **"Deploy to Hugging Face Spaces"**.
- Tu peux le relancer manuellement (bouton "Re-run all jobs") ou simplement faire une petite modification dans un fichier de ton projet (comme ajouter un espace dans le `README.md`) puis faire un `git push`.
- L'Action va s'exécuter. Si tu regardes les logs de l'Action, tu verras qu'elle pousse ton code vers `projet-8-api` puis vers `projet-8-app`.

**C'est fini ! 🎉**
Dès que l'Action est terminée, retourne sur tes pages Hugging Face. Elles passeront du statut "Building" à "Running", et ton application complète sera en ligne !

*Rappel : Si tu ne visites pas ton application pendant 48 heures, Hugging Face la mettra en pause pour économiser de l'énergie. Il suffira de retourner sur la page et de cliquer sur "Restart" pour la réveiller en 2 minutes.*
