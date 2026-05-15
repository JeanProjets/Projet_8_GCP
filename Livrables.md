# Livrables


Les scripts développés sur un notebook permettant l’exécution du pipeline complet :
Ce livrable vous servira à présenter le caractère “industrialisable” de votre travail en particulier le générateur de données.
Une API (Flask ou FastAPI) déployée sur le Cloud (Azure, Heroku, PythonAnywhere ou toute autre solution), pour exposer votre modèle entraîné et qui recevra en entrée une image et retournera le mask prédit (les segments identifiés par votre modèle) :
Ce livrable permettra à Laura d’utiliser facilement votre modèle.
Une application (Flask, Streamlit) de présentation des résultats qui consomme l’API de prédiction, déployée sur le Cloud (Azure, Heroku, PythonAnywhere ou toute autre solution). Cette application sera l’interface pour tester l’API et intégrera les fonctionnalités suivantes :  affichage de la liste des id des images disponibles, lancement de la prédiction du mask pour l’id sélectionné par appel à l’API, et affichage de l’image réelle, du mask réel et du mask prédit :
Ce livrable permettra d’illustrer votre travail auprès de vos collègues
Une note technique de 10 pages environ contenant une présentation des différentes approches et une synthèse de l’état de l’art, la présentation plus détaillée du modèle et de l’architecture retenue, une synthèse des résultats obtenus (incluant les gains obtenus avec les approches d’augmentation des données) et une conclusion avec des pistes d’amélioration envisageables  :
Ce livrable vous servira à présenter votre démarche technique à vos collègues.
Un support de présentation (type Power Point) de votre démarche méthodologique (30 slides maximum) :
Ce livrable vous permettra de présenter vos résultats à Laura.
Déposez sur la plateforme, dans un dossier zip nommé “Titre_du_projet_nom_prénom”, votre livrable nommé comme suit : Nom_Prénom_n° du livrable_nom du livrable_date de démarrage du projet. Cela donnera : 

Nom_Prénom_1_scripts_mmaaaa
Nom_Prénom_2_API_mmaaaa
Nom_Prénom_3_application_Flask_mmaaaa
Nom_Prénom_4_note_technique_mmaaaa
Nom_Prénom_5_presentation_mmaaaa
Par exemple, votre premier livrable peut être nommé comme suit : Dupont_Jean_1_scripts_012024.

 

# Soutenance:


Pendant la soutenance, l’évaluateur ne jouera aucun rôle en particulier. Vous lui présenterez l’ensemble de votre travail. 

Présentation (20 minutes) 
Présentation du contexte, des objectifs, des principes de segmentation et des mesures de performance qui seront utilisées pour comparer les modèles (5 minutes)
Présentation des différents modèles, simulations et comparaisons des modèles (10 minutes).
Mise en production d’un modèle (5 minutes) :
Architecture API et application Web et démarche de mise en production sur le Cloud choisi par l’étudiant
démonstration de fonctionnement de l’application et de la prédiction de segmentation d’une image (mask).
Discussion (5 minutes)
L’évaluateur vous challengera sur vos choix. 
Débriefing (5 minutes)
À la fin de la soutenance, vous pourrez débriefer ensemble. 
Votre présentation devrait durer 20 minutes (+/- 5 minutes).  Puisque le respect des durées des présentations est important en milieu professionnel, les présentations en dessous de 15 minutes ou au-dessus de 25 minutes peuvent être refusées. 

Concernant la mise en production de l’API, plusieurs solutions s’offrent à vous, en particulier Azure webapp, AWS et Heroku. À vous de choisir la solution qui vous convient le mieux.

Dans le cadre de l’utilisation de Heroku, étant devenu payant depuis fin novembre 2022, les coûts liés à votre projet seront à votre charge. Vous êtes donc libre de vous investir financièrement si vous le souhaitez, mais vous n’avez aucune obligation de le faire pour réaliser ce projet. 

Quelque soit la solution Cloud choisie, l'étudiant et l'évaluateur veilleront à enregistrer pendant la soutenance la démo de l'application en production, ce qui permettra au jury de visionner cette démo, sans que l'étudiant n'ait à maintenir son application sur le Cloud. Maintenir l’application dans le Cloud pourrait en effet engendrer des coûts. 