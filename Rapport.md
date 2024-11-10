# Rapport de Projet : Analyse des Modèles de Prédiction pour le DPE
## 1. Introduction
Le projet réalisé s'inscrit dans le cadre du défi Enedis, visant à établir le lien entre les diagnostics de performance énergétique (DPE) et la consommation réelle d'électricité des logements. L'objectif principal est d'évaluer la précision des prévisions issues des DPE par rapport aux consommations réelles et de quantifier les économies potentielles après amélioration des DPE.  

Dans ce rapport, nous nous concentrerons sur l'élaboration des différents modèles.


## 2. Démarche et modèles testés


## 3. Présentation des Modèles Utilisés
### 3.1 Modèle de Classification de la classe énergétique pour le DPE
Ce modèle vise à prédire la classe DPE d'un logement à l'aide de la fonction MLPClassifier() de scikit-learn.

Configuration du Modèle
```python
classifier = MLPClassifier(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001)
```
Variables Prédictives
Générales : code postal, période de construction, type de logement, surface habitable, nombre d'étages, hauteur sous plafond.
Consommation : type de chauffage, type d'énergie pour l'eau chaude, consommation totale annuelle, consommation pour le chauffage, consommation pour l'eau chaude.


### 3.2 Modèle de Régression pour la Consommation Énergétique
Ce modèle, utilisant MLPRegressor(), vise à prédire la consommation réelle d'énergie d'un logement.

Configuration du Modèle
```python
regressor = MLPRegressor(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001)
```
Variables Prédictives
Générales : mêmes que pour le modèle de classification.
Consommation : type de chauffage, type d'énergie pour l'eau chaude, classe énergétique.


## 4. Résultats des Tests
### 4.1 Précision de la Classification
Nous avons testé le MLPClassifier() sur des données du Rhône, obtenant une précision de 0,93 avant optimisation et 0,95 après.

### 4.2 Précision de la Régression
[Résultats à compléter : tests en cours.]


## 5. Conclusions et Améliorations Futures
Les premiers résultats montrent une bonne performance pour la classification. Des optimisations supplémentaires pour le modèle de régression et l'intégration d'autres modèles comme les forêts aléatoires pourraient être envisagées.