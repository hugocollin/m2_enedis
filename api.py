import pandas as pd
import requests

class API:
    # Méthode pour charger une page de données
    def get_data_page(self, url):
        response = requests.get(url)

        # Vérification du statut de la réponse
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erreur lors de la récupération des données : [{response.status_code}] {response.text}")

    # Méthode pour récupérer les données
    def get_data(self):
        print("Détection des nouveaux DPE en cours...")
        all_dpe = []
        page_number = 1 

        # Identification des nouveaux DPE
        while True:
            try:
                if page_number == 1:
                    dpe = self.get_data_page("https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q=69&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29&select=N%C2%B0DPE%2CDate_r%C3%A9ception_DPE")
                else:
                    dpe = self.get_data_page(url)

                # Ajout des données
                all_dpe.extend(dpe["results"])
                
                # Récupération de l'URL de la page suivante
                url = dpe.get("next")
                if not url:
                    break

                page_number += 1
            except Exception as e:
                print(f"Erreur lors du traitement : {str(e)}")
                break

        # Transformation des données en DataFrame
        all_dpe = pd.DataFrame(all_dpe)

        # Mise en forme des données
        all_dpe = all_dpe.drop(columns=["_score"])
        all_dpe["Date_réception_DPE"] = all_dpe["Date_réception_DPE"].str.replace("-", "")

        # Si des données sont déjà présentes
        try:
            all_data = []
            df = pd.read_csv("assets/data_69.csv", sep="|")
            
            # Récupération de la date des DPE les plus récents
            max_date = df["Date réception DPE"].max()
            
            # Filtrage des nouveaux DPE
            all_dpe = all_dpe[all_dpe["Date_réception_DPE"] > str(max_date)]
            
            # Si aucun nouveau DPE n'est trouvé, arrêt de la fonction
            if all_dpe.empty:
                print("Aucun nouveau DPE trouvé")
                return

            print(f"{len(all_dpe)} nouveaux DPE trouvés : récupération des données en cours, cela peut prendre un moment...")
            
            # Récupération de tous les N°DPE
            dpe_list = all_dpe["N°DPE"].tolist()
            
            # Division de la liste en chunks de 500
            for i in range(0, len(dpe_list), 100):
                chunk = dpe_list[i:i + 100]
                dpe_str = '%2C'.join(map(str, chunk))
                try :
                    data = self.get_data_page(f"https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q={dpe_str}&q_fields=N%C2%B0DPE&select=P%C3%A9riode_construction%2CSurface_habitable_logement%2CNombre_niveau_logement%2CType_b%C3%A2timent%2CHauteur_sous-plafond%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CConso_5_usages_%C3%A9_finale%2CConso_chauffage_%C3%A9_finale%2CConso_ECS_%C3%A9_finale%2CClasse_altitude%2CEtiquette_DPE%2CNom__commune_(BAN)%2CCode_postal_(BAN)%2CDate_r%C3%A9ception_DPE%2C_geopoint")
                    
                    # Ajout des données
                    all_data.extend(data["results"])
                except Exception as e:
                    print(f"Erreur lors du traitement : {str(e)}")
                    break  

            # Transformation des données en DataFrame
            all_data = pd.DataFrame(all_data)

            # Mise en forme des données
            all_data = all_data.drop(columns=["_score"])
            all_data[["Latitude", "Longitude"]] = all_data["_geopoint"].str.split(",", expand=True)
            all_data = all_data.drop(columns=["_geopoint"])
            all_data["Date_réception_DPE"] = all_data["Date_réception_DPE"].str.replace("-", "")
            all_data["Date_réception_DPE_graph"] = all_data["Date_réception_DPE"].str[:6]
            all_data = all_data.rename(columns={
                "Conso_5_usages_é_finale": "Consommation totale",
                "Nom__commune_(BAN)": "Nom commune",
                "Date_réception_DPE": "Date réception DPE",
                "Conso_ECS_é_finale": "Consommation ECS",
                "Code_postal_(BAN)": "Code postal",
                "Hauteur_sous-plafond": "Hauteur sous-plafond",
                "Surface_habitable_logement": "Surface habitable logement",
                "Nombre_niveau_logement": "Nombre niveau logement",
                "Période_construction": "Période construction",
                "Conso_chauffage_é_finale": "Consommation chauffage",
                "Type_bâtiment": "Type bâtiment",
                "Classe_altitude": "Classe altitude",
                "Type_énergie_principale_ECS": "Type énergie ECS",
                "Type_énergie_principale_chauffage": "Type énergie chauffage",
                "Etiquette_DPE": "Étiquette DPE"
                })
            
            # Ajout des nouvelles données au fichier data_69.csv
            all_data.to_csv("assets/data_69.csv", index=False, sep="|", encoding="utf-8", mode="a", header=False)

            print(f"{len(dpe_list)} DPE ajoutés")
            
        except FileNotFoundError:
            # Récupération des données complètes si le fichier n'existe pas
            while True:
                try:
                    if page_number == 1:
                        data = self.get_data_page("https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q=69&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29&select=P%C3%A9riode_construction%2CSurface_habitable_logement%2CNombre_niveau_logement%2CType_b%C3%A2timent%2CHauteur_sous-plafond%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CConso_5_usages_%C3%A9_finale%2CConso_chauffage_%C3%A9_finale%2CConso_ECS_%C3%A9_finale%2CClasse_altitude%2CEtiquette_DPE%2CNom__commune_(BAN)%2CCode_postal_(BAN)%2CDate_r%C3%A9ception_DPE%2C_geopoint")
                        total_rows = data.get("total")
                        print(f"{len(total_rows)} nouveaux DPE trouvés : récupération des données en cours, cela peut prendre un moment...")
                    else:
                        data = self.get_data_page(url)

                    # Ajout des données
                    all_data.extend(data["results"])
                    
                    # Récupération de l'URL de la page suivante
                    url = data.get("next")
                    if not url:
                        break

                    page_number += 1
                except Exception as e:
                    print(f"Erreur lors du traitement : {str(e)}")
                    break

            # Transformation des données en DataFrame
            all_data = pd.DataFrame(all_data)

            # Mise en forme des données
            all_data = all_data.drop(columns=["_score"])
            all_data[["Latitude", "Longitude"]] = all_data["_geopoint"].str.split(",", expand=True)
            all_data = all_data.drop(columns=["_geopoint"])
            all_data["Date_réception_DPE"] = all_data["Date_réception_DPE"].str.replace("-", "")
            all_data["Date_réception_DPE_graph"] = all_data["Date_réception_DPE"].str[:6]
            all_data = all_data.rename(columns={
                "Conso_5_usages_é_finale": "Consommation totale",
                "Nom__commune_(BAN)": "Nom commune",
                "Date_réception_DPE": "Date réception DPE",
                "Conso_ECS_é_finale": "Consommation ECS",
                "Code_postal_(BAN)": "Code postal",
                "Hauteur_sous-plafond": "Hauteur sous-plafond",
                "Surface_habitable_logement": "Surface habitable logement",
                "Nombre_niveau_logement": "Nombre niveau logement",
                "Période_construction": "Période construction",
                "Conso_chauffage_é_finale": "Consommation chauffage",
                "Type_bâtiment": "Type bâtiment",
                "Classe_altitude": "Classe altitude",
                "Type_énergie_principale_ECS": "Type énergie ECS",
                "Type_énergie_principale_chauffage": "Type énergie chauffage",
                "Etiquette_DPE": "Étiquette DPE"
                })
            
            # Sauvegarde des données en CSV
            all_data.to_csv("assets/data_69.csv", index=False, sep="|", encoding="utf-8")

            print(f"{total_rows} DPE ajoutés")
    
    # Méthode pour obtenir les coordonnées géographiques d'un code postal
    def get_coordinates(self, code_postal):
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'postalcode': code_postal,
            'country': 'France',
            'format': 'json'
        }
        headers = {
            'User-Agent': 'm2-enedis'
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
        return None, None

    # Méthode pour obtenir l'altitude d'un point géographique
    def get_altitude(lat, lon):
        url = 'https://api.open-elevation.com/api/v1/lookup'
        params = {
            'locations': f'{lat},{lon}'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                return data['results'][0]['elevation']
        return None

    def get_average_temperature(self, code_postal):
        """
        Récupère la température moyenne d'une commune basée sur son code postal en utilisant l'API OpenWeatherMap.
        """
        # [TEMP] POur faire fonctionner le code
        # from api import API
        # code_postal = '13080'
        # moyenne_temp = API().get_average_temperature(code_postal)

        # if moyenne_temp is not None:
        #     print(f"La température moyenne pour le code postal {code_postal} est de {moyenne_temp:.2f}°C.")
        # else:
        #     print("Impossible de récupérer la température moyenne.")

        # Récupération des coordonnées géographiques
        lat, lon = self.get_coordinates(code_postal)
        if lat is None or lon is None:
            print("Coordonnées non trouvées pour le code postal fourni.")
            return None

        # Appel de l'API OpenWeatherMap
        url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {
            'lat': lat,
            'lon': lon,
            'appid': 'deba5862a5629eebfb2e8a8d2108e4d6',
            'units': 'metric',
            'lang': 'fr'
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération des données météo : {response.status_code}")
            return None

        data = response.json()

        # Extraction de la température
        temperatures = []
        for entry in data.get('list', []):
            temp = entry.get('main', {}).get('temp')
            if temp is not None:
                temperatures.append(temp)

        if not temperatures:
            print("Aucune donnée de température disponible.")
            return None

        # Calcul de la température moyenne
        average_temp = sum(temperatures) / len(temperatures)

        return average_temp