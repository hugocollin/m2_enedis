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
- [Description de l'application](#description_app)
- [Modèles utilisés](#modeles)
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
Lancez l'interface Dash avec les données récupérées :
```python
python main.py
```

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
model = MLPClassifier(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001)
```
Le modèle pour la prédiction de la consommation est toujours en work in progress
        
## Tests
Cette section a pour but de tester le code afin de montrer un exemple
-- à faire

## Contribution
Les contributions sont les bienvenues ! Pour contribuer :

Forkez le projet.
Créez votre branche de fonctionnalité (``` git checkout -b feature/AmazingFeature ```).
Commitez vos changements (``` git commit -m 'Add some AmazingFeature' ```).
Poussez à la branche (``` git push origin feature/AmazingFeature ```).
Ouvrez une Pull Request.

## Auteurs
Ce projet a été développé par 3 étudiants du Master 2 SISE : Hugo COLLIN, Maxence LIOGIER et Antoine ORUEZABALA
