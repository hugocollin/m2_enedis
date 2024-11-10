# Rapport de Projet : Analyse des Modèles de Prédiction pour le DPE
## 1. Introduction
Le projet réalisé s'inscrit dans le cadre du défi Enedis, visant à établir le lien entre les diagnostics de performance énergétique (DPE) et la consommation réelle d'électricité des logements. L'objectif principal est d'évaluer la précision des prévisions issues des DPE par rapport aux consommations réelles et de quantifier les économies potentielles après amélioration des DPE.  

Dans ce rapport, nous nous concentrerons sur l'élaboration des différents modèles.


## 2. Démarche et modèles testés
### 2.1 Démarche de test
Pour tous les modèles que nous avons testés, la démarche que nous avons suivie est similaire.  
Nous avons sélectionné les données du département du Rhône (69) comme données d'entrainement et de test. Puis, nous avons utilisé la validation croisée pour tester les modèles.  

Pour prédire la classe énergétique et la consommation, nous avons fait le choix d'utiliser deux modèles différents : une classification et une régression respectivement car il ne nous a pas paru possible de réaliser des modèles performants pouvant prédire les deux et donc ne prenant ni l'un ni l'autre en entrée.  Ainsi chaque modèle utilise comme variable d'entrée la cible de l'autre (la conso pour calculer le DPE et le DPE pour calculer la conso).

Comme indicateurs, nous avons pris la précision pour la classification et le RMSE pour la régression.


### 2.2 Modèle de Classification de la classe énergétique pour le DPE
Le modèle de classification est le premier sur lequel nous nous sommes penchés. C'est sans doute sur lui que le plus d'essais ont été effectués avant de trouver le modèle final.  

Les premiers modèles qui ont été testés sont la régression logistique, l'arbre de décision et la forêt aléatoire.  
Parmi ces modèles, l'arbre de décision a été celui qui a donné les résultats les plus satisfaisants en obtenant une précision de 0,93.
Pour cela, nous avons utilisé les variables prédictives suivantes :
- infos générales : nom commune du logement, niveau de vie médian dans la commune, type de logement, surface habitable, nombre d'étages, hauteur sous plafond
- infos sur la consommation : type de chauffage, type d'énergie pour l'eau chaude, conso totale sur l'année, conso en chauffage, conso en eau chaude  

Toutes ces données ont été trouvées sur le site de l'Ademe à l'exception du niveau de vie médian par commune qui lui a été récupéré via le site de l'insee : https://statistiques-locales.insee.fr/#c=indicator&i=filosofi.med&s=2021&t=A01&view=map1. Nous avons fait le choix de l'inclure car nous supposons qu'il est plus facile de rénover son logement lorsque nous avons un bon niveau de vie que lorsque c'est moins le cas.  
A ce moment là, nous n'utilisions pas l'année de construction car 40% des logements dans les données du Rhône n'avaient pas cette colonne de remplie. Pour contourner ce problème, nous avons par la suite utilisé la période de construction qui est quant à elle beaucoup plus exhaustive. La période de construction semble importante car les anciens logements sont mieux isolés que les anciens grâce aux différentes réglementations (RT2012, RE2020)  
Pour améliorer encore plus le modèle, nous avons récupéré l'altitude de chaque commune à l'aide de l'API de open elevation : https://api.open-elevation.com/api/v1/lookup.  
Suite à cela, nous nous sommes rendus compte que demander un nom de commune à l'utilisateur est désagréable  car il y a un risque d'erreur trop important (majuscules, tirets, espaces, fautes d'orthographe...). C'est pourquoi nous avons décidé de ne demander que les codes postaux.  
C'est à la suite de toutes ces étapes que nous avons obtenu le score de 0,93.

Enfin, nous avons testé deux autres modèles : le gradient boosting et un réseau de neurone. (GradientBoostingClassifier et MLPClassifier).
Parmi ces deux modèles, le MLPClassifier est celui ayant donné le meilleur résultat avec une précision de 0,95. Ce score a été obtenu suite à une optimisation des hyper-paramètres à l'aide d'un grid search
```python
param_grid_rf = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
}
```
Voici donc la configuration du modèle final :
```python
classifier = MLPClassifier(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001)
```
De plus, ce modèle étant bien plus petit en taille que l'arbre de décision, il a permis de prendre moins de place sur le site et ainsi d'optimiser son fonctionnement. 


### 2.3 Modèle de Régression pour la Consommation Énergétique
Afin de prédire la consommation d'énergie d'un logement, nous avons utilisé un modèle de régression.  
Pour construire ce modèle, nous avons décidé d'utiliser les mêmes variables prédictive que le précédent mais en retirant toutes les variables liées à la consommation (c'est ce que l'on veut prédire) et en les remplacant par la classe énergétique du logement. Voici donc la synthèse des variables retenues pour ce modèle :
- infos générales : code postal, niveau de vie médian dans la commune, altitude, période de construction, type de logement, surface habitable, nombre d'étages, hauteur sous plafond
- infos sur la consommation : type de chauffage, type d'énergie pour l'eau chaude, classe énergétique du logement  

Afin de choisir le meilleur modèle, nous en avons testé plusieurs, tous présents dans la bibliothèque scikit learn : RidgeCV, RandomForestRegressor, GradientBoostingRegressor, MLPRegressor.  
Au final, parmi ces modèles, celui qui a réussi à avoir le meilleur résultat est ici aussi le réseau de neurones (MLPRegressor).
[A VERIFIER QUE CELA NE CHANGE PAS]  
Pour déterminer les hyper-paramètres, nous avons une fois encore réalisé un grid search
[INSERER GRIDSEARCH ICI]

Voici donc la configuration du modèle final :
```python
regressor = MLPRegressor(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001)
```  

Cependant, contrairement au modèle de classification qui donnait des résultats très satisfaisants, le modèle de régression ne donne pas de résultat réellement à la hauteur.
[DONNER LE RESULTAT, QUEL RMSE ?]


## 3. Conclusions et Améliorations Futures
### Conclusions
Dans le cadre de ce projet, nous avons exploré différentes approches pour prédire la classe énergétique (DPE) et la consommation réelle d'électricité des logements. Nous avons testé plusieurs modèles et avons finalement retenu un modèle de classification basé sur un réseau de neurones (MLPClassifier) pour prédire la classe énergétique et un modèle de régression (MLPRegressor) pour estimer la consommation énergétique.  

Le modèle de classification a montré des résultats très satisfaisants avec une précision de 0,95, ce qui indique une très bonne capacité à prédire la classe énergétique des logements. En revanche, le modèle de régression n'a pas atteint les performances escomptées, avec un RMSE de [INSERER RMSE ICI], suggérant que des améliorations sont nécessaires pour mieux prédire la consommation énergétique.  


### Améliorations Futures
Pour améliorer les performances des modèles, plusieurs pistes peuvent être envisagées :

1. **Enrichissement des Données** : Intégrer des données supplémentaires, telles que les caractéristiques climatiques ou les habitudes de consommation des occupants, pourrait améliorer la précision des prédictions.

2. **Modèles Hybrides** : Combiner plusieurs modèles (par exemple, en utilisant des modèles d'ensemble) pourrait permettre de capturer des relations complexes dans les données et d'améliorer les performances globales.

3. **Analyse des Erreurs** : Une analyse plus approfondie des erreurs de prédiction pourrait révéler des schémas ou des biais spécifiques, permettant d'ajuster les modèles en conséquence.

En conclusion, bien que des résultats prometteurs aient été obtenus, notamment avec le modèle de classification, des efforts supplémentaires sont nécessaires pour améliorer la prédiction de la consommation énergétique. Les pistes d'amélioration mentionnées ci-dessus offrent des directions potentielles pour les travaux futurs, avec l'objectif ultime de fournir des outils de prédiction fiables et utiles pour les particuliers et les décideurs en matière de rénovation énergétique.