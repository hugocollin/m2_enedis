import pandas as pd
import requests

class API:
    # Méthode pour charger une page de données
    def get_data(self, county):
        response = requests.get(f"https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q={county}&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29&select=P%C3%A9riode_construction%2CSurface_habitable_logement%2CNombre_niveau_logement%2CType_b%C3%A2timent%2CHauteur_sous-plafond%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CConso_5_usages_%C3%A9_finale%2CConso_chauffage_%C3%A9_finale%2CConso_ECS_%C3%A9_finale%2CClasse_altitude%2CEtiquette_DPE%2CAdresse_(BAN)%2CNom__commune_(BAN)%2CCode_postal_(BAN)%2C_geopoint")

        # Vérification du statut de la réponse
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erreur lors de la récupération des données : [{response.status_code}] {response.text}")

    # Méthode pour récupérer les données
    def get_all_data(self, county):
        all_data = []
        page_number = 1 
        total_lines = 0

        while True:
            try:
                if page_number == 1:
                    data = self.get_data()
                else:
                    data = self.get_data(county)
                lines_added = len(data["results"])
                all_data.extend(data["results"])
                total_lines += lines_added
                
                print(f"Page {page_number} traitée : {lines_added} lignes ajoutées ({total_lines} lignes récupérées au total)")
                
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

        return all_data