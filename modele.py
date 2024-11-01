import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def modele(df):
    """
    Cette fonction a pour but de construire un modèle prédisant la classe énergétique d'un logement
    :param df: dataframe contenant les données de départ, avec toutes les colonnes sélectionnées lors du scrapping de l'API
    """
    # On enlève des colonnes, soit inutiles soit trop de na
    col_a_suppr = ['Adresse_(BAN)', '_geopoint', 'Année_construction', 'Nombre_niveau_logement']
    df.drop(columns=col_a_suppr, inplace=True, errors='ignore')
    
    # on retire les na
    df = df.dropna()

    # définition de la variable cible pour ne pas le réécrir à chaque fois
    target = 'Etiquette_DPE'

    # Définition des cibles / 
    y = df[target]
    X = df.drop(columns=[target])

    # découpage train_test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, stratify = y, random_state = 0)

    # Créer et entraîner le modèle
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Je ne sais pas s'il faut les garder
    accuracy = accuracy_score(y_test, y_pred)
    mc = pd.crosstab(y_test, y_pred, colnames=['pred'], rownames=['obs'], margins=True)

    return y_pred

if __name__ == "__main__":
    df = pd.read_csv(f'data/data_69.csv', sep='|')
    modele(df)