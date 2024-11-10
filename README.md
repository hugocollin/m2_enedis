# README : Projet Enedis

## Description
Ce projet s'inscrit dans le cadre du défi proposé par Enedis, visant à montrer le lien entre les diagnostics de performance énergétique (DPE) et les consommations réelles d'électricité des logements. Les objectifs principaux sont de quantifier l'impact des améliorations de DPE sur les économies d'énergie et de vérifier la fiabilité des prévisions du DPE par rapport aux données réelles. L'enjeu est d'aider les particuliers et les décideurs à mieux évaluer les bénéfices d'une rénovation énergétique.  

Pour cela, nous avons développé une web application (dash) permettant de présenter les résultats que nous avons obtenus. La structure de cette application est décrite plus loin.  

Les données utilisées viennent de l'API de l'Ademe.  
Lorsque vous lancerez la web application, les données présentées par défaut sont celles du département du Rhône (69) mais il vous sera possible de choisir un autre département.  


## Table des Matières
- [Description](#description)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Description de l'application](#description-de-lapplication)
- [Modèles utilisés](#modèles-utilisés)
- [Tests](#tests)
- [Contribution](#contribution)
- [Auteurs](#auteurs)  


## Installation
Pour installer ce projet, suivez ces étapes :
1) Assurez vous d'avoir python installé sur votre machine avec une version 3.9+ (à vérifier).

2) Clonez le dépôt :
```bash
git clone https://github.com/hugocollin/m2_enedis
```

3) Installez les dépendances :
```bash
pip install -r requirements.txt  
```

## Utilisation
Ce projet étant une web application, il y a deux manière de le lancer : en ligne ou en local.

Si vous voulez le lancer en local :
- Lancez l'interface Dash avec les données récupérées :
```python
python main.py
```
- Cliquez sur l'URL qui apparaît. Un exemple pourrait être http://127.0.0.1:8050  

Si vous voulez le lancer en ligne :
- Allez sur cet URL : https://m2-enedis.onrender.com/  


## Description de l'application 
L'application s'organise en 4 onglets : Contexte, Modèles, Visualisations et Prédictions.  
- Contexte présente le projet et la notion de DPE
- Modèles permet de charger de nouvelles données à partir de l'API de l'Ademe et de réentraîner les modèles de prédiction à partir de nouvelles données.
- Visualisations présente les données sous forme de tableau, de graphiques et de carte afin d'obtenir plusieurs indicateurs tels que le DPE ou la consommation.
- Prédictions permet d'interroger les modèles que nous avons construits afin de prédire la consommation ou bien le DPE de son logement.  


## Modèles utilisés
Afin de prédire le DPE, nous avons utilisé un modèle de réseau neuronal.  
Pour cela, nous avons utilisé la fonction MLPClassifier() de scikit learn. Voici la ligne python permettant de définir notre modèle :  
```python
classifier = MLPClassifier(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001)
```
Pour utiliser ce premier modèle, voici les variables prédictives que nous avons sélectionnées :
- infos générales : code postal, niveau de vie médian dans la commune, altitude, période de construction, type de logement, surface habitable, nombre d'étages, hauteur sous plafond
- infos sur la consommation : type de chauffage, type d'énergie pour l'eau chaude, conso totale sur l'année, conso en chauffage, conso en eau chaude

Nous avons construit un second modèle permettant de prédire la consommation. 
Pour cela, nous avons également utilisé un réseau neuronal. Mais là où le premier modèle était une classification, le second est une regression.  
C'est pourquoi nous avons utilisé cette fois-ci la fonction MLPRegressor() de scikit learn.
```python
regressor = MLPRegressor(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001
 ```
[ATTENTION, CE MODELE PEUT CHANGER]  
Pour ce modèle, nous avons utilisé les variables prédictives suivantes :
- infos générales : code postal, niveau de vie médian dans la commune, altitude, période de construction, type de logement, surface habitable, nombre d'étages, hauteur sous plafond
- infos sur la consommation : type de chauffage, type d'énergie pour l'eau chaude, classe énergétique du logement  

A savoir que le niveau de vie et l'altitude ne sont pas demandés à l'utilisateurs mais sont interrogés à partir du code postal.


## Tests
Nous avons utilisé les données du département du Rhône comme données d'entraînement et de test en utilisant des validations croisées.  

Pour tester les modèles de classification, nous avons utilisé la précision (accuracy) comme indicateur.  En utilisant MLPClassifier, nous avons obtenu, d'abord sans optimisation, une précision de 0,93. Après avoir optimisé les hyperparamètres, ce score est monté à environ 0,95. Cela est très satisfaisant puisque cela signifie que 95% des prédictions sont correctes.  

Pour la régression, nous avons utilisé le RMSE (root mean squared error) comme indicateur. En utilisant MLPRegressor, nous avons obtenu un RMSE de 40000. Nous sommes beaucoup plus mitigés sur ce point puisque cela signifie que, en moyenne, les prédictions du modèle s'écartent de 40 000 kWh/an des valeurs réelles. Pour donner un ordre de grandeur, une maison individuelle consomme en moyenne entre 10000 et 25000kwh/an.  


## Contribution
Les contributions sont les bienvenues ! Pour contribuer :
- Forkez le projet.
- Créez votre branche de fonctionnalité (```git checkout -b feature/AmazingFeature```).
- Commitez vos changements (```git commit -m 'Add some AmazingFeature'```).
- Poussez à la branche (```git push origin feature/AmazingFeature```).
- Ouvrez une Pull Request.  


## Auteurs
Ce projet a été développé par 3 étudiants du Master 2 SISE : Hugo COLLIN, Maxence LIOGIER et Antoine ORUEZABALA
