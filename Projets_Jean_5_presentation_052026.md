# Support de Présentation - Future Vision Transport
**Soutenance Projet 8 : Modèle de Segmentation pour Système Embarqué**

> **Note pour Jean** : Tu pourras copier-coller ce contenu dans un PowerPoint ou Google Slides. Chaque titre `# Slide X` correspond à une diapositive.

---

# Slide 1 : Titre
**Segmentation Sémantique pour Véhicules Autonomes**
*Future Vision Transport - Équipe R&D*
Présenté par : Jean Projets
Date : Mai 2026

# Slide 2 : Le Contexte et les Objectifs
- **Le besoin de l'entreprise** : Équiper nos véhicules autonomes d'une "vision" capable de comprendre l'environnement urbain.
- **Mon rôle** : Concevoir le module de **Segmentation des images** (Étape 3 du pipeline global).
- **Le cahier des charges (Laura & Franck)** :
    - Regrouper les catégories complexes en 8 classes essentielles.
    - Créer une API simple qui prend une image et renvoie un masque prédictif.
    - S'assurer que le tout s'intègre facilement (Industrialisation / MLOps).

# Slide 3 : Le Jeu de Données et Prétraitement
- **Dataset utilisé** : Cityscapes (Images de caméras embarquées en Europe).
- **Le défi** : 32 sous-catégories (ex: mur, clôture, poteau, feu tricolore, panneau, bâtiment...).
- **La solution** : Fusion des masques via la librairie `albumentations` pour obtenir **8 classes** : 
    - *Vide, Sol, Construction, Objet, Nature, Ciel, Humain, Véhicule*.

# Slide 4 : L'Augmentation de Données (Data Augmentation)
- **Pourquoi l'utiliser ?** Éviter le surapprentissage (overfitting) et augmenter la diversité du dataset d'entraînement.
- **La méthode** : Au lieu de stocker des milliers d'images modifiées sur le disque, nous les modifions *à la volée* (on-the-fly) grâce à un "Générateur" Python.
- **Les transformations appliquées** :
    - Rotations aléatoires (simulation de la topographie).
    - Flips horizontaux (simulation d'inversion du sens de la route).
    - Variations de contraste (simulation d'éclairages différents).

# Slide 5 : Théorie : Qu'est-ce que l'architecture U-Net ?
- **Pourquoi U-Net ?** C'est le standard de l'industrie pour la segmentation sémantique (à l'origine créé pour l'imagerie médicale).
- **Comment ça marche ?** Sa forme en "U" :
    - **1. La Contraction (Encodeur)** : Le réseau "compresse" l'image pour comprendre *CE QUI* est présent (extraction de caractéristiques).
    - **2. L'Expansion (Décodeur)** : Le réseau "décompresse" l'image pour comprendre *OÙ* c'est présent (localisation).
    - **3. Les Skip Connections** : Les raccourcis qui relient la gauche et la droite du "U" pour ne pas perdre la précision des contours.

# Slide 6 : Le Transfer-Learning (Notre solution optimisée)
- **Le problème du U-Net classique** : L'encodeur part de zéro, il met un temps infini à apprendre ce qu'est une forme de voiture ou de route.
- **La solution (Transfer Learning)** : Nous avons remplacé l'encodeur par **MobileNetV2**.
- **Pourquoi MobileNet ?**
    - Il a déjà été entraîné sur des millions d'images (ImageNet). Il "sait" déjà voir.
    - Il est conçu pour les architectures mobiles/embarquées (très léger, peu de calculs mathématiques).
    - Il permet au réseau de se focaliser uniquement sur l'apprentissage du Décodeur (le coloriage final).

# Slide 7 : Comparaison des Modèles et Résultats
- **Modèle 1 : U-Net classique**
    - Apprentissage lent, poids lourd.
    - Peine à détourer correctement les petits objets (piétons).
- **Modèle 2 : U-Net + MobileNet (Transfer Learning)**
    - Convergence très rapide.
    - Temps d'inférence (ms/image) optimisé pour l'embarqué.
    - Les résultats sur le set de test montrent une bien meilleure netteté (IoU supérieur).
- *(Insérer ici une capture d'écran d'une image originale VS Masque réel VS Prédiction)*

# Slide 8 : L'Architecture MLOps (L'industrialisation)
- Pour que "Laura" puisse utiliser le modèle, il faut l'encapsuler et le déployer.
- **L'API** : Développement d'un microservice avec **FastAPI** (très performant, documentation Swagger intégrée).
- **L'Application de test** : Développement d'un tableau de bord **Streamlit** pour tester les inférences en un clic.
- **Conteneurisation** : Chaque composant est isolé dans un **Docker**.

# Slide 9 : Le Déploiement Cloud et le CI/CD
- **Le défi technique** : Les modèles Deep Learning pèsent lourd (plusieurs dizaines de Mo). Déployer sur GitHub et des serveurs Cloud (Render/GCP) pose de grandes contraintes de stockage et de coût.
- **La solution hybride GitHub <-> Hugging Face** :
    - Le code maître est centralisé sur **GitHub**.
    - Utilisation d'un pipeline d'**Intégration Continue (GitHub Actions)**.
    - Le fichier `sync-to-hub.yml` utilise Python pour transférer les modèles et le code directement sur **Hugging Face Spaces**.
    - **Résultat** : Un déploiement automatisé, gratuit, et sans limites de stockage Git.

# Slide 10 : Démonstration en Direct
- *[Note pour la présentation : Clique sur ce lien pendant la soutenance pour montrer le résultat]*
- URL de l'App (Streamlit) : [https://huggingface.co/spaces/JeanProjets/projet-8-app](https://huggingface.co/spaces/JeanProjets/projet-8-app)
- **Important (Si l'application est en veille)** : Hugging Face met les applications inactives en veille au bout de 48h. Si vous voyez "Space Asleep" ou "Paused", il suffit de cliquer sur le bouton bleu **"Restart this Space"** (au milieu de la page). L'application sera relancée en 2 minutes. N'oubliez pas de le faire quelques minutes avant l'arrivée du jury !

# Slide 11 : Conclusion
- Les objectifs sont atteints : Modèle de segmentation entraîné et industrialisé via une API REST fonctionnelle.
- Les gains de l'architecture choisie : Le Transfer-Learning (MobileNet) a prouvé son efficacité face au U-Net standard.
- L'infrastructure MLOps est robuste et prête pour de futures itérations.

# Slide 12 : Pistes d'Amélioration Futures
- **Quantification TFLite** : Alléger davantage le modèle (Float16) pour le CPU du véhicule.
- **Post-traitement** : Ajout d'algorithmes (CRF) pour lisser les contours prédits.
- **Moteur de décision** : Connecter l'API FastAPI au module de décision (Freinage d'urgence, maintien dans la voie).
- *Merci de votre attention !*
