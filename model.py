from api import API

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

class Model:
    def train_model(df, local_data, county):
        """
        Cette fonction permet de créer un modèle de classification de l'étiquette DPE
        """
        if local_data:
            # Chargement des données locales
            df = pd.read_csv(f'data/data_69.csv', sep='|')
        else:
            # Récupération des données
            df = API.get_all_data(county)

        # Suppresion des colonnes informatives
        del_col = ['Adresse_(BAN)', 'Nom__commune_(BAN)', '_geopoint']
        df.drop(columns=del_col, inplace=True, errors='ignore')
        
        # Suppression des lignes avec des valeurs manquantes
        df = df.dropna()

        # Préparation des données pour le modèle
        df = pd.get_dummies(df, columns=['Période_construction', 'Type_bâtiment', 'Type_énergie_principale_chauffage', 'Type_énergie_principale_ECS', 'Classe_altitude'])

        # Définition des variables explicatives et de la variable cible
        y = df["Etiquette_DPE"]
        X = df.drop(columns=["Etiquette_DPE"])

        # Normalisation des données
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        # Séparation des données en jeu d'entraînement et jeu de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, stratify=y, random_state = 0)

        # Création du modèle et recherche sur grille
        model = MLPClassifier(random_state=0, hidden_layer_sizes=(100, 50), learning_rate_init=0.001, max_iter=300, tol=0.0001)
        model.fit(X_train, y_train)

        # Sauvegarde du modèle et du scaler
        joblib.dump(model, 'model/mlp_model.pkl')
        joblib.dump(scaler, 'model/scaler.pkl')

        # Évaluation du modèle
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Précision du modèle : {accuracy}")

    def predict_model(input_data):
        """
        Cette fonction permet de faire une prédiction de la classe énergétique
        """

        # Chargement du modèle et du scaler
        model = joblib.load('model/mlp_model.pkl')
        scaler = joblib.load('model/scaler.pkl')

        # Transformation de l'information "Année de construction" en "Période de construction"
        if input_data['Période_construction'] < 1948:
            input_data['Période_construction'] = 'avant 1948'
        elif input_data['Période_construction'] >= 1948 and input_data['Période_construction'] <= 1974:
            input_data['Période_construction'] = '1948-1974'
        elif input_data['Période_construction'] >= 1975 and input_data['Période_construction'] <= 1977:
            input_data['Période_construction'] = '1975-1977'
        elif input_data['Période_construction'] >= 1978 and input_data['Période_construction'] <= 1982:
            input_data['Période_construction'] = '1978-1982'
        elif input_data['Période_construction'] >= 1983 and input_data['Période_construction'] <= 1988:
            input_data['Période_construction'] = '1983-1988'
        elif input_data['Période_construction'] >= 1989 and input_data['Période_construction'] <= 2000:
            input_data['Période_construction'] = '1989-2000'
        elif input_data['Période_construction'] >= 2001 and input_data['Période_construction'] <= 2005:
            input_data['Période_construction'] = '2001-2005'
        elif input_data['Période_construction'] >= 2006 and input_data['Période_construction'] <= 2012:
            input_data['Période_construction'] = '2006-2012'
        elif input_data['Période_construction'] >= 2013 and input_data['Période_construction'] <= 2021:
            input_data['Période_construction'] = '2013-2021'
        else:
            input_data['Période_construction'] = 'Après 2021'
        
        # Application des mêmes transformations que lors de l'entraînement
        input_data = pd.get_dummies(input_data, columns=['Période_construction', 'Type_bâtiment', 'Type_énergie_principale_chauffage', 'Type_énergie_principale_ECS', 'Classe_altitude'])
        input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)
        input_data = scaler.transform(input_data)

        # Prédiction
        prediction = model.predict(input_data)
        return prediction[0]