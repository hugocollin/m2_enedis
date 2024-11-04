import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

def modele(df):
    """
    Cette fonction a pour but de construire un modèle prédisant la classe énergétique d'un logement
    :param df: dataframe contenant les données de départ, avec toutes les colonnes sélectionnées lors du scrapping de l'API
    """
    # Suppresion des colonnes informatives
    del_col = ['Adresse_(BAN)', 'Nom__commune_(BAN)', '_geopoint']
    df.drop(columns=del_col, inplace=True, errors='ignore')
    
    # Suppression des lignes avec des valeurs manquantes
    df = df.dropna()

    # Définition de la variable cible
    target = 'Etiquette_DPE'

    # Préparation des données pour le modèle
    df = pd.get_dummies(df, columns=['Période_construction', 'Type_bâtiment', 'Type_énergie_principale_chauffage', 'Type_énergie_principale_ECS', 'Classe_altitude'])

    # Définition des variables explicatives et de la variable cible
    y = df[target]
    X = df.drop(columns=[target])

    # Normalisation des données
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Séparation des données en jeu d'entraînement et jeu de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, stratify=y, random_state = 0)

    # Création du modèle et recherche sur grille
    model = MLPClassifier(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calcul de la précision du modèle
    accuracy = accuracy_score(y_test, y_pred)
    mc = pd.crosstab(y_test, y_pred, colnames=['pred'], rownames=['obs'], margins=True)

    print(f"Précision du modèle : {accuracy}")
    print(mc)

    return y_pred

if __name__ == "__main__":
    df = pd.read_csv(f'data/data_69.csv', sep='|')
    modele(df)