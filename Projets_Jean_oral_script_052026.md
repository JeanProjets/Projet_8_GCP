# Script de Soutenance Oral - Projet 8
**Conception d'un Modèle de Segmentation pour Système Embarqué**  
*Ingénieur IA - Future Vision Transport*  

---

> [!TIP]
> **Conseils généraux pour la soutenance (20 minutes au total) :**
> - **Le timing est crucial** : Si vous passez en dessous de 15 minutes ou au-dessus de 25 minutes, l'évaluateur peut pénaliser votre prestation. Ce script est calibré pour durer environ **19 à 20 minutes** en parlant à un rythme posé.
> - **L'intonation** : Variez votre ton. Insistez bien sur les mots **en gras** pour maintenir l'attention de l'évaluateur.
> - **Les pauses** : Prenez le temps de respirer entre chaque transition de slide.
> - **Démo live** : Assurez-vous d'avoir ouvert l'application Hugging Face (et de l'avoir réveillée si nécessaire) dans un onglet séparé *avant* le début de la soutenance.

---

## Chronologie recommandée
*   **Partie 1 : Contexte, objectifs et métriques (Slides 1 à 7)** : ~4 minutes 30 secondes
*   **Partie 2 : Modélisation, comparaisons et résultats (Slides 8 à 20)** : ~10 minutes 30 secondes
*   **Partie 3 : MLOps, déploiement et démonstration (Slides 21 à 30)** : ~5 minutes

---

# PARTIE 1 : CONTEXTE, OBJECTIFS ET MÉTRIQUES (00:00 - 04:30)

## Slide 1 : Titre
*   **Durée recommandée** : 20 secondes
*   **Action** : Afficher la page de garde. Regarder l'évaluateur avec un visage ouvert et chaleureux.
*   **Texte à prononcer** :
    > "Bonjour à tous. Je suis ravi de vous présenter aujourd'hui mon travail sur le **Projet 8** de mon parcours d'Ingénieur IA. Ce projet s'inscrit au sein de notre entreprise fictive **Future Vision Transport** et porte sur la conception, l'entraînement et la mise en production d'un **modèle de segmentation sémantique d'images** destiné à être intégré dans un système embarqué pour véhicules autonomes."

---

## Slide 2 : Le Contexte de l'Entreprise (Future Vision Transport)
*   **Durée recommandée** : 35 secondes
*   **Action** : Cliquer sur la flèche pour passer à la diapositive suivante.
*   **Texte à prononcer** :
    > "Pour poser le contexte, rappelons que **Future Vision Transport** conçoit des technologies de pointe pour les véhicules autonomes. Le traitement d'images y joue un rôle absolument capital. 
    > 
    > Les flux vidéo captés en temps réel par les caméras du véhicule doivent être analysés instantanément. C'est l'étape 3 du pipeline de vision globale qui m'a été confiée : le module de **segmentation sémantique**. Sa tâche est de donner des "yeux" et un "cerveau" à la voiture pour catégoriser chaque pixel de l'image captée et guider le système de décision."

---

## Slide 3 : Problématique & Cahier des Charges
*   **Durée recommandée** : 45 secondes
*   **Action** : Regarder la slide et l'évaluateur pour marquer la transition sur les besoins métier.
*   **Texte à prononcer** :
    > "Le cahier des charges qui m'a été communiqué par nos collègues, Laura et Franck, comprend plusieurs piliers clés :
    > 
    > Premièrement, concevoir un modèle de Deep Learning avec une **précision spatiale élevée** pour identifier les éléments essentiels de la route.
    > 
    > Deuxièmement, adapter la granularité des étiquettes pour simplifier les calculs en regroupant les catégories de départ en **8 classes fondamentales**.
    > 
    > Troisièmement, encapsuler ce modèle dans une **API REST FastAPI** pour que Laura puisse consommer les prédictions facilement.
    > 
    > Et enfin, développer un **dashboard interactif Streamlit** pour tester notre API et montrer son efficacité lors d'une démonstration industrialisée."

---

## Slide 4 : Le Jeu de Données : Cityscapes
*   **Durée recommandée** : 35 secondes
*   **Action** : Montrer du doigt ou avec le curseur les dimensions des images.
*   **Texte à prononcer** :
    > "Pour répondre à ce besoin, nous travaillons sur le jeu de données de référence de l'industrie : **Cityscapes**. Ce dataset regroupe des images stéréo prises depuis des caméras embarquées dans des environnements urbains de dizaines de villes allemandes. 
    > 
    > La résolution native est très élevée : **1024 par 2048 pixels**, avec des annotations de masques extrêmement méticuleuses au pixel près. Le défi réside dans la complexité de départ, car Cityscapes propose **32 sous-catégories d'origine**, allant de la plaque d'immatriculation au garde-fou."

---

## Slide 5 : Simplification : Regroupement en 8 Classes
*   **Durée recommandée** : 40 secondes
*   **Action** : Balayer rapidement les 8 classes pour montrer la structure simplifiée.
*   **Texte à prononcer** :
    > "Pour rendre le modèle compatible avec les ressources de calcul limitées d'un processeur embarqué, Franck a demandé de fusionner ces 32 catégories complexes en **8 classes clés** :
    > 
    > Nous avons donc le **Void** pour le capot ou l'arrière-plan flou ; le **Flat** qui représente la route et le trottoir ; le **Construction** pour les bâtiments et ponts ; l'**Object** pour les feux et panneaux de signalisation ; la **Nature** pour les arbres et buissons ; le **Sky** pour le ciel ; et enfin, les deux catégories les plus critiques pour la sécurité : **Human** pour les piétons ou cyclistes, et **Vehicle** pour les voitures et transports en commun."

---

## Slide 6 : Analyse Exploratoire des Données (EDA)
*   **Durée recommandée** : 45 secondes
*   **Action** : Prendre un ton plus technique pour expliquer le diagnostic des données.
*   **Texte à prononcer** :
    > "Lors de mon analyse exploratoire (l'EDA), j'ai dressé un constat mathématique majeur : le **class imbalance** ou déséquilibre des classes. 
    > 
    > En moyenne, la route et les bâtiments occupent plus de **60 %** de l'espace visuel d'une scène routière, alors que les éléments cruciaux comme les piétons, les vélos ou la signalisation représentent **moins de 2 %** des pixels. 
    > 
    > Si nous entraînons un réseau de neurones brut sur ces données sans précaution, le modèle aura tendance à ignorer les piétons tout en conservant une excellente "précision" statistique apparente. Ce biais statistique est extrêmement dangereux pour un véhicule autonome."

---

## Slide 7 : Métrique Clé de Performance : Le Mean IoU
*   **Durée recommandée** : 50 secondes
*   **Action** : Insister sur la formule et la rigueur scientifique.
*   **Texte à prononcer** :
    > "Pour contourner ce problème, l'Accuracy classique (pourcentage de pixels bien prédits) a été écartée car elle est trompeuse. À la place, j'ai sélectionné la métrique standard en segmentation sémantique : l'**Intersection over Union** (le score de Jaccard), que nous calculons sous sa forme de moyenne : le **Mean IoU**.
    > 
    > Le mIoU calcule la zone de chevauchement entre la prédiction et la réalité divisée par leur union, et ce, de manière **indépendante pour chacune des 8 classes**. Ainsi, une erreur de détection sur un piéton aura exactement le même poids sur le score final qu'une erreur sur une immense surface de route. C'est le seul juge de paix fiable pour valider la robustesse de nos modèles."

---

# PARTIE 2 : MODÉLISATION, SIMULATIONS & COMPARAISONS (04:30 - 15:00)

## Slide 8 : Prévention du Surapprentissage : La Data Augmentation
*   **Durée recommandée** : 40 secondes
*   **Action** : Respirer et marquer la transition vers la partie technique de modélisation.
*   **Texte à prononcer** :
    > "Passons à présent à la phase de modélisation. Pour éviter le surapprentissage de notre réseau de neurones sur les scènes routières figées de l'entraînement, j'ai mis en place une solide stratégie de **Data Augmentation**.
    > 
    > En segmentation, nous faisons face à une contrainte stricte : toute transformation géométrique sur l'image caméra doit être appliquée **au pixel près et à l'identique** sur le masque d'annotation. Pour cela, j'ai utilisé la bibliothèque spécialisée `albumentations` qui intègre ces transformations duales de manière native et synchrone."

---

## Slide 9 : Détails des Transformations Appliquées
*   **Durée recommandée** : 35 secondes
*   **Action** : Énoncer calmement les types d'augmentations.
*   **Texte à prononcer** :
    > "Concrètement, quelles sont les transformations appliquées à la volée ?
    > 
    > Nous avons des transformations **géométriques** comme le flip horizontal aléatoire pour simuler un changement du sens de circulation, et des micro-rotations pour simuler les secousses de la voiture. 
    > 
    > Et nous avons des transformations **photométriques** pour modifier la luminosité et le contraste de l'image sans altérer le masque. Cela immunise notre modèle contre les variations de météo ou le passage dans les zones d'ombres."

---

## Slide 10 : Algorithmes : L'Architecture U-Net (Théorie)
*   **Durée recommandée** : 50 secondes
*   **Action** : Expliquer clairement le dessin ou le principe du "U".
*   **Texte à prononcer** :
    > "En ce qui concerne le choix de l'algorithme, j'ai opté pour l'architecture **U-Net**, qui est la référence absolue en segmentation d'images. 
    > 
    > Le réseau est structuré en deux branches symétriques : 
    > 
    > D'abord, la branche de gauche : l'**Encodeur**, ou chemin de contraction. C'est un CNN classique qui réduit la dimension spatiale de l'image tout en extrayant des filtres sémantiques profonds (pour savoir *CE QU'* il y a dans l'image).
    > 
    > Ensuite, la branche de droite : le **Décodeur**, ou chemin d'expansion. C'est un réseau de convolutions inversées qui agrandit les cartes sémantiques pour restaurer la taille spatiale d'origine (pour savoir *OÙ* se trouvent ces éléments)."

---

## Slide 11 : Le Rôle des Skip Connections
*   **Durée recommandée** : 45 secondes
*   **Action** : Utiliser un ton enthousiaste pour cette astuce architecturale.
*   **Texte à prononcer** :
    > "Mais le secret du U-Net réside dans les **Skip Connections**, ces flèches horizontales qui relient l'encodeur au décodeur. 
    > 
    > Lors de la compression dans l'encodeur, les coordonnées précises des pixels et les détails géométriques fins sont irrémédiablement perdus. Les skip connections court-circuitent le réseau en copiant directement les cartes de caractéristiques haute résolution de l'encodeur pour les concaténer au décodeur. 
    > 
    > Grâce à cela, le décodeur dispose d'informations sémantiques globales, mais aussi de coordonnées géométriques chirurgicales, ce qui permet de détourer proprement les contours des objets."

---

## Slide 12 : Pipeline de Données : Le Data Generator Keras
*   **Durée recommandée** : 45 secondes
*   **Action** : Insister sur l'aspect "industrialisable" du code.
*   **Texte à prononcer** :
    > "Sur le plan de l'ingénierie logicielle, charger des centaines d'images de 1024x2048 en mémoire sature instantanément n'importe quel ordinateur ou puce embarquée. 
    > 
    > J'ai donc conçu un **générateur de données asynchrone** en héritant de la classe `Sequence` de Keras. Ce générateur charge les données par batch à la volée depuis le disque. Il s'occupe de redimensionner les images en **256 par 512 pixels** (un excellent compromis pour le CPU embarqué), applique la data augmentation, effectue le mapping dynamique des 32 classes vers nos 8 classes et encode les masques en one-hot vector."

---

## Slide 13 : Les Fonctions de Perte (Loss Functions)
*   **Durée recommandée** : 45 secondes
*   **Action** : Expliquer les ajustements mathématiques pour contrer le déséquilibre.
*   **Texte à prononcer** :
    > "Pour l'apprentissage, la fonction de perte par défaut est la **Categorical Cross-Entropy**. Bien qu'efficace, elle souffre du déséquilibre des classes en négligeant les petites classes. 
    > 
    > Pour y remédier, j'ai testé des approches avec la **Dice Loss**, qui maximise le taux de chevauchement. Finalement, j'ai combiné une Categorical Cross-Entropy avec un ajustement précis des poids de classe et un taux d'apprentissage adapté à l'aide de l'optimiseur Adam. 
    > 
    > Cela a permis de forcer la rétropropagation à pénaliser lourdement les erreurs faites sur les classes minoritaires comme les humains et les véhicules."

---

## Slide 14 : Première Modélisation : U-Net classique "from scratch"
*   **Durée recommandée** : 40 secondes
*   **Action** : Présenter la baseline.
*   **Texte à prononcer** :
    > "Ma première approche a été de concevoir et d'entraîner un modèle **U-Net classique construit de toutes pièces**. 
    > 
    > Cet encodeur custom comporte 4 blocs de convolutions, Batch Normalization et Max Pooling. Il possède environ **2 millions de paramètres** que j'ai entraînés avec des poids initialisés de manière aléatoire. C'est notre modèle 'baseline' de référence."

---

## Slide 15 : Analyse & Limites de la Baseline
*   **Durée recommandée** : 50 secondes
*   **Action** : Adopter une posture critique et analytique face aux résultats.
*   **Texte à prononcer** :
    > "Les limites de cette baseline 'from scratch' sont rapidement apparues. 
    > 
    > D'une part, la convergence à l'entraînement a été particulièrement lente. Le modèle doit tout apprendre par lui-même, depuis l'identification d'une simple ligne droite ou d'une texture de béton jusqu'à la forme complexe d'une voiture. 
    > 
    > D'autre part, sur le plan qualitatif, si le modèle dessine correctement la route et le ciel, il est incapable de segmenter proprement les petits éléments. Les piétons sont flous, voire invisibles, et les poteaux ou panneaux routiers sont hachés. C'est une limite critique pour notre cas d'usage."

---

## Slide 16 : Seconde Modélisation : Le Transfer Learning
*   **Durée recommandée** : 45 secondes
*   **Action** : Sourire et présenter le pivot méthodologique réussi.
*   **Texte à prononcer** :
    > "Pour dépasser ces limites et accélérer notre démarche technique, j'ai pivoté vers le **Transfer Learning**.
    > 
    > L'idée est simple mais extrêmement puissante : au lieu de laisser notre modèle démarrer avec des poids aléatoires et "aveugles", nous lui greffons un encodeur qui a déjà appris à observer des millions d'images réelles du dataset ImageNet. Le modèle sait déjà repérer les formes complexes, les ombres, les cercles et les textures. Il ne lui reste plus qu'à apprendre à assembler ces connaissances pour notre tâche de segmentation."

---

## Slide 17 : MobileNetV2 comme Encodeur (Backbone)
*   **Durée recommandée** : 50 secondes
*   **Action** : Argumenter sur le choix de l'efficacité embarquée.
*   **Texte à prononcer** :
    > "J'ai spécifiquement choisi **MobileNetV2** comme colonne vertébrale, ou backbone, de notre encodeur. 
    > 
    > Pourquoi ? Parce que MobileNet est la référence absolue pour le matériel embarqué. Il s'appuie sur des convolutions séparables en profondeur, les **Depthwise Separable Convolutions**. 
    > 
    > En séparant le filtrage spatial de la combinaison des canaux, il permet d'obtenir des performances de vision exceptionnelles tout en réduisant par 9 le coût en opérations mathématiques et en mémoire par rapport à des réseaux lourds comme VGG ou ResNet. C'est l'atout parfait pour la réactivité à bord du véhicule."

---

## Slide 18 : Connexion MobileNetV2 et Décodeur U-Net
*   **Durée recommandée** : 40 secondes
*   **Action** : Décrire brièvement l'assemblage technique.
*   **Texte à prononcer** :
    > "J'ai donc extrait le tronc de MobileNetV2 pré-entraîné, en congelant ses premiers blocs pour conserver les détecteurs de formes universels. 
    > 
    > J'ai repéré et connecté ses couches intermédiaires (les blocs 1, 3 et 6) pour alimenter les skip connections de notre décodeur personnalisé. C'est une architecture hybride très élégante, à la fois extrêmement légère en poids et redoutable d'efficacité à l'entraînement."

---

## Slide 19 : Comparaison Quantitative des Modèles
*   **Durée recommandée** : 1 minute
*   **Action** : Analyser les lignes du tableau comparatif avec précision.
*   **Texte à prononcer** :
    > "Les résultats quantitatifs sont sans appel et valident notre démarche technique.
    > 
    > Le modèle U-Net classique from scratch nécessite plus de 40 époques pour converger vers un **mIoU de validation décevant de 0.42**, avec un temps d'inférence de **120 millisecondes sur CPU**, ce qui est trop lent.
    > 
    > Notre modèle **U-Net combiné à MobileNetV2** a convergé en seulement 15 époques. Son poids a été divisé par 3, tombant à seulement **12 Mo**. Son mIoU sur le jeu de test s'envole à **0.68**, et surtout, son temps d'inférence est descendu à **35 millisecondes par image**. C'est le seuil symbolique du temps réel sur processeur embarqué !"

---

## Slide 20 : Comparaison Qualitative de la Segmentation
*   **Durée recommandée** : 45 secondes
*   **Action** : Décrire visuellement l'amélioration des masques.
*   **Texte à prononcer** :
    > "Visuellement, la différence est saisissante. 
    > 
    > Là où le U-Net custom affichait des masques pixelisés et instables, le U-Net MobileNetV2 produit des délimitations très propres. La séparation entre la route et le trottoir est nette, et les véhicules sont parfaitement isolés. 
    > 
    > Mais le plus satisfaisant reste la détection stable des piétons, même à moyenne distance. Le modèle a développé une excellente compréhension spatiale des scènes urbaines."

---

## Slide 21 : Gain Réel de la Data Augmentation
*   **Durée recommandée** : 45 secondes
*   **Action** : Exposer les résultats de l'étude d'ablation pour légitimer la rigueur du projet.
*   **Texte à prononcer** :
    > "Pour isoler et quantifier le gain réel de la Data Augmentation, j'ai mené une étude d'ablation en entraînant le modèle avec et sans ces transformations à la volée.
    > 
    > Sans augmentation, nous observons un surapprentissage marqué : le mIoU sur les données d'entraînement grimpe en flèche mais stagne sur le jeu de validation. 
    > 
    > En activant les rotations, les flips et le contraste, nous avons gagné **8 points de mIoU global sur le jeu de test**. Cela prouve scientifiquement l'apport capital de cette technique de régularisation pour immuniser notre IA contre les aléas de la route réelle."

---

# PARTIE 3 : MLOPS, DÉPLOIEMENT & DÉMONSTRATION (15:00 - 20:00)

## Slide 22 : Architecture MLOps (Vue d'ensemble)
*   **Durée recommandée** : 40 secondes
*   **Action** : Passer à la Partie 3. Adopter une attitude dynamique et fière de l'industrialisation.
*   **Texte à prononcer** :
    > "Avoir un excellent modèle sur notre notebook n'est qu'une première étape. Pour répondre aux besoins de Laura et industrialiser mon travail, j'ai conçu et mis en place une architecture **MLOps découplée** basée sur des microservices.
    > 
    > D'un côté, nous avons le client : une application Web Streamlit interactive. De l'autre, le serveur : notre API FastAPI qui charge le modèle Keras en mémoire et effectue les calculs. L'image caméra transite par une requête HTTP POST sécurisée et le serveur renvoie le masque colorisé directement."

---

## Slide 23 : L'API REST de Prédiction avec FastAPI
*   **Durée recommandée** : 45 secondes
*   **Action** : Mettre en avant la robustesse du framework FastAPI.
*   **Texte à prononcer** :
    > "L'API a été développée avec **FastAPI**. J'ai retenu ce framework pour sa rapidité asynchrone légendaire et sa génération automatique d'une documentation interactive Swagger UI.
    > 
    > L'endpoint principal est `/segmentation`. J'ai utilisé le mécanisme de **lifespan** de FastAPI pour charger le modèle Keras en mémoire une seule fois au démarrage de l'API. Lors d'un appel, l'API reçoit le flux binaire, le convertit en tableau Numpy, applique le prétraitement, effectue la prédiction et renvoie le masque sous forme de flux PNG asynchrone via une `StreamingResponse` pour maximiser le débit."

---

## Slide 24 : Conteneurisation de l'API & de l'App (Docker)
*   **Durée recommandée** : 35 secondes
*   **Action** : Expliquer l'isolation de l'environnement.
*   **Texte à prononcer** :
    > "Pour garantir que notre code s'exécute de façon strictement identique en local et sur nos serveurs de production, j'ai conteneurisé chaque brique à l'aide de **Docker**.
    > 
    > J'ai écrit deux fichiers Dockerfile distincts : un pour isoler l'API FastAPI et ses dépendances lourdes (TensorFlow, Keras), et un second pour l'interface de démonstration Streamlit. Cela élimine définitivement les conflits de versions système."

---

## Slide 25 : Le Défi des Modèles Volumineux sur le Cloud
*   **Durée recommandée** : 45 secondes
*   **Action** : Présenter la contrainte technique résolue intelligemment.
*   **Texte à prononcer** :
    > "Lors de la mise en production, j'ai fait face à un défi d'infrastructure classique : les fichiers de modèles de Deep Learning pèsent très lourd. Notre modèle optimisé pèse 12 Mo, mais d'autres itérations dépassent largement les 100 Mo.
    > 
    > GitHub bloque les fichiers de plus de 100 Mo par défaut. De plus, les hébergeurs Cloud traditionnels imposent des limites strictes de stockage sur leurs serveurs gratuits, ce qui compliquait notre déploiement."

---

## Slide 26 : La Solution de CI/CD Hybride via GitHub Actions
*   **Durée recommandée** : 50 secondes
*   **Action** : Détailler le workflow automatique.
*   **Texte à prononcer** :
    > "J'ai donc mis en place une architecture de **CI/CD hybride astucieuse** en exploitant la plateforme **Hugging Face Spaces**.
    > 
    > Notre code source est versionné sur **GitHub**. À chaque validation de code (`git push`), un workflow automatique **GitHub Actions** est déclenché. Il exécute un script Python qui utilise l'API de Hugging Face pour pousser programmatiquement les fichiers de code et le modèle Keras volumineux directement dans les conteneurs de production HF. 
    > 
    > Le service est ainsi mis à jour de manière transparente, sécurisée et entièrement gratuite."

---

## Slide 27 : Le Dashboard Streamlit (Interface de Démo)
*   **Durée recommandée** : 45 secondes
*   **Action** : Présenter le fonctionnement du client Streamlit.
*   **Texte à prononcer** :
    > "L'interface finale destinée à nos collègues a été construite avec **Streamlit**. 
    > 
    > Elle se connecte à notre flotte d'images de test réelles issues de Cityscapes. L'utilisateur sélectionne un ID d'image dans un menu déroulant, clique sur un bouton pour l'envoyer à l'API FastAPI, et l'interface affiche instantanément l'image caméra, le masque parfait attendu pour comparaison et la prédiction en direct de notre modèle."

---

## Slide 28 : Démonstration de l'Application en Action
*   **Durée recommandée** : 15 secondes
*   **Action** : Montrer la capture d'écran sur la slide, puis **basculer immédiatement sur l'onglet du navigateur** où l'application Streamlit tourne en direct !
*   **Texte à prononcer** :
    > "Voici un aperçu visuel de l'application en action. Je vais maintenant basculer sur mon navigateur pour vous faire une démonstration en direct de ce pipeline d'inférence en production."

---

### [LANCEMENT DE LA DÉMO EN DIRECT - DURÉE : 1 MINUTE 30]
*   **Actions à réaliser pendant la démo** :
    1.  **Vérifier** que la page Streamlit est bien chargée (si elle s'est mise en veille, cliquez sur "Restart this Space" en amont).
    2.  **Ouvrir** le menu latéral gauche et sélectionnez un fichier, par exemple `bielefeld_000000_000321_leftImg8bit.png`.
    3.  **Cliquer** sur le bouton bleu **"Lancer l'Inférence de l'API"**.
    4.  **Commenter pendant le chargement (qui dure moins de 5 secondes)** : 
        > *"Vous voyez ici que l'image caméra s'affiche à gauche. À droite, notre API FastAPI hébergée sur un autre espace a reçu l'image, l'a segmentée en 35 millisecondes et a renvoyé ce masque PNG colorisé. Le vert représente la végétation, le violet la route, le bleu le ciel et le rouge la présence d'humains ou de véhicules."*
    5.  **Rebasculer sur le diaporama** pour la suite et fin du script.

---

## Slide 29 : Liens du Déploiement en Production
*   **Durée recommandée** : 20 secondes
*   **Action** : Montrer brièvement les liens et préciser le mécanisme de veille.
*   **Texte à prononcer** :
    > "Comme vous pouvez le voir, l'API et l'application sont hébergées de manière autonome et découplée sur Hugging Face Spaces. L'ensemble de la chaîne est opérationnel et prêt pour des tests de plus grande envergure par nos ingénieurs."

---

## Slide 30 : Conclusion, Perspectives & Améliorations Futures
*   **Durée recommandée** : 1 minute
*   **Action** : Adopter un ton posé et professionnel pour conclure en beauté. Regarder l'évaluateur.
*   **Texte à prononcer** :
    > "Pour conclure, ce projet valide la faisabilité complète d'un pipeline de vision sémantique : depuis l'acquisition des données brutes avec un générateur asynchrone robuste, jusqu'à la mise en production de microservices hautement performants grâce au Transfer Learning et à une infrastructure MLOps moderne.
    > 
    > En termes de perspectives, mes priorités pour la prochaine itération sont :
    > 
    > Premièrement, la **quantification post-entraînement** pour convertir notre modèle Keras en format **TensorFlow Lite (TFLite)** avec une précision en Float16 ou Int8. Cela divisera par 4 le poids du modèle (qui tombera à 3 Mo) et augmentera la cadence d'inférence embarquée.
    > 
    > Deuxièmement, l'intégration d'un lissage spatial par **CRF** en post-traitement pour affiner davantage les contours géométriques.
    > 
    > Et enfin, la connexion directe de l'API avec le module de décision de freinage d'urgence du véhicule.
    > 
    > Je vous remercie pour votre attention et je suis à présent à votre entière disposition pour répondre à vos questions et échanger sur nos choix techniques."
