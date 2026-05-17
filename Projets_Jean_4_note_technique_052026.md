# Note Technique - Future Vision Transport
**Projet 8 : Conception d'un modèle de segmentation d'images pour systèmes embarqués**

**Auteur :** Jean Projets
**Date :** Mai 2026

---

## 1. Contexte et Objectifs
Future Vision Transport développe des systèmes embarqués de vision par ordinateur pour les véhicules autonomes. L'objectif de ce projet est de concevoir, entraîner et mettre en production un premier modèle de segmentation sémantique d'images. Ce modèle doit s'intégrer de manière fluide dans la chaîne de décision du véhicule, en ingérant les flux des caméras embarquées pour isoler et identifier les différents éléments de l'environnement (véhicules, piétons, route, ciel, etc.).

Le jeu de données utilisé est *Cityscapes* (images annotées de caméras embarquées en environnement urbain).

## 2. Prétraitement et Data Augmentation

### 2.1 Regroupement des Classes
Le jeu de données *Cityscapes* original contient 32 sous-catégories, ce qui est beaucoup trop granulaire et complexe pour une première itération temps-réel. Pour répondre aux contraintes du pipeline d'acquisition, nous avons opéré un regroupement ("mapping") des classes pour les réduire à **8 catégories principales** (void, flat, construction, object, nature, sky, human, vehicle). Ce re-mapping s'effectue automatiquement lors de la phase de création du générateur de données via la librairie `albumentations` et des masques `labelIds`.

### 2.2 Augmentation de Données
Pour prévenir le surapprentissage (overfitting) et augmenter la robustesse de notre réseau de neurones face aux différents environnements urbains, nous avons implémenté une augmentation des données à la volée ("on-the-fly") lors de l'entraînement. 
Lorsqu'une image de route ou de véhicule est passée au modèle, elle subit des transformations géométriques :
- **Rotations aléatoires** (pour simuler l'inclinaison de la voiture ou des pentes).
- **Flips horizontaux** (effet miroir pour inverser le sens de circulation ou les paysages).
- **Ajustement de la luminosité/contraste** (pour simuler des conditions météorologiques variées).

## 3. Architecture des Modèles (U-Net)

L'architecture choisie est le **U-Net**, particulièrement adapté à la segmentation d'images biomédicales et urbaines, car il capture à la fois le contexte global et la précision de localisation.

### 3.1 U-Net "Custom" (from scratch)
Nous avons d'abord conçu une architecture U-Net standard :
- **Encodeur (Contraction)** : Une série de convolutions (`Conv2D`) couplées à des fonctions de pooling (`MaxPooling`) pour extraire les "features" (formes, textures) de l'image tout en réduisant sa dimensionnalité spatiale.
- **Décodeur (Expansion)** : Une série de convolutions transposées (`UpSampling2D`) pour reconstruire l'image à sa taille originelle. 
- **Skip Connections** : Des connexions résiduelles qui relient les couches de l'encodeur à celles du décodeur pour ne pas perdre la précision des contours lors de la reconstruction.

### 3.2 U-Net avec Transfer Learning (MobileNetV2)
Pour optimiser les performances et la rapidité du modèle (contrainte critique pour les systèmes embarqués), nous avons implémenté un deuxième modèle basé sur le **Transfer-Learning**. 
Au lieu d'utiliser un encodeur construit de zéro, nous avons injecté un modèle **MobileNetV2** pré-entraîné sur ImageNet en guise d'encodeur. MobileNetV2 est spécifiquement conçu pour les architectures mobiles et embarquées (très léger en paramètres, calculs optimisés par convolution séparable). Ce modèle permet une extraction de caractéristiques (feature extraction) bien plus robuste et rapide.

## 4. Résultats et Comparaison des Modèles

Les performances ont été évaluées principalement sur la fonction de perte (Loss) et la précision catégorielle (Accuracy).

1. **U-Net Simple** : Bien qu'il converge et apprenne la structure d'une route, l'entraînement est long, très lourd, et le modèle peine à distinguer les objets de taille réduite (piétons, petits panneaux).
2. **U-Net + MobileNet (Transfer Learning)** : L'utilisation de l'encodeur pré-entraîné a drastiquement accéléré la phase d'apprentissage. Le réseau a pu se focaliser immédiatement sur la tâche de segmentation (Décodeur). Les contours des véhicules et des routes sont beaucoup plus nets. L'inférence est également beaucoup plus rapide en ms/image, répondant ainsi au cahier des charges de "Laura".

*Note : Les masques de validation montrent que les gains obtenus par la data augmentation (rotation) permettent au modèle de bien généraliser sur des images de validation (Test-set).*

## 5. Industrialisation et MLOps (CI/CD)

### 5.1 Environnement de Déploiement
Le modèle final a été intégré dans une API robuste développée avec le framework **FastAPI**. Ce choix a été motivé par la rapidité asynchrone du framework et sa documentation auto-générée (Swagger).
L'interface de démonstration a été développée en **Streamlit** pour permettre aux équipes de tester visuellement l'inférence.

### 5.2 Architecture et Git
Tout le projet est centralisé sur un dépôt **GitHub**. 
Cependant, l'utilisation d'outils cloud traditionnels rencontrait un obstacle majeur : la taille des fichiers de modèles Deep Learning (`best_unet_model.keras` dépasse 20 Mo, d'autres peuvent dépasser les 100 Mo de limite de GitHub).

### 5.3 L'Intégration Continue (GitHub Actions vers Hugging Face)
Pour contourner ce problème sans payer de serveurs onéreux (Render/GCP), nous avons conçu une architecture astucieuse en utilisant **Hugging Face Spaces**.
- L'infrastructure s'appuie sur deux conteneurs Docker séparés (un pour l'API, un pour l'App Streamlit).
- **Pipeline CI/CD** : Un script `sync-to-hub.yml` (GitHub Actions) a été écrit. À chaque validation (`git push`) sur la branche principale, les serveurs de GitHub exécutent un script Python exploitant la bibliothèque `huggingface_hub`. Ce script pousse programmatiquement le code source et les modèles (même s'ils pèsent plusieurs centaines de Mo, contournant la limite de Git) directement sur les serveurs de Hugging Face.
- L'API et l'Application redémarrent alors automatiquement dans le cloud pour refléter la nouvelle version.

## 6. Conclusion et Pistes d'Amélioration
Le système de segmentation actuel démontre la faisabilité technique du pipeline : de l'acquisition des données au déploiement en ligne d'une API capable d'interagir avec d'autres microservices.
**Améliorations futures envisagées :**
- **Quantification** : Convertir le modèle Keras en TFLite (float16 ou int8) pour diviser par 4 le poids du modèle et accélérer l'inférence sur le CPU embarqué du véhicule.
- **Optimisation des prédictions** : Ajouter des algorithmes de type CRF (Conditional Random Fields) en post-traitement pour lisser les contours des objets (véhicules, piétons) segmentés par l'IA.
