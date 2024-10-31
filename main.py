from api import API
import pandas as pd

def recup_api(county):
    """
    Cette fonction sert à requêter l'api de l'ademe pour en extraire les données selon un département
    """
    # Instanciation de la classe avec l'URL de base
    api = API(f"https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q={county}&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29&select=Ann%C3%A9e_construction%2CSurface_habitable_logement%2CNombre_niveau_logement%2CType_b%C3%A2timent%2CHauteur_sous-plafond%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CConso_5_usages_%C3%A9_finale%2CConso_chauffage_%C3%A9_finale%2CConso_ECS_%C3%A9_finale%2CClasse_altitude%2CEtiquette_DPE%2CAdresse_(BAN)%2CNom__commune_(BAN)%2CCode_postal_(BAN)%2C_geopoint")

    # Récupération des données
    all_data = api.get_all_data()

    # Création du DataFrame
    df = pd.DataFrame(all_data)

    return df


def main(county, from_api):
    """
    Ceci est la fonction principale
    :param county: numéro de département
    :param is_api: booléen, si True alors on récupère les données de l'api sinon directement récupéré
    """
    if from_api :
        df = recup_api(county)
    else:
        df = pd.read_csv(f'data_{county}.csv')
    
    return df


if __name__ == "__main__":
    main(county='69', from_api=False)