# Connexions aux fichiers du projet
from api import API
from interface import DashInterface

# Importation des librairies nécessaires
import pandas as pd

# # Paramètres de la requête
# county = input("Entrez le numéro du département : ")

# # Instanciation de la classe avec l'URL de base
# api = API(f"https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q={county}&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29&select=Ann%C3%A9e_construction%2CSurface_habitable_logement%2CNombre_niveau_logement%2CType_b%C3%A2timent%2CHauteur_sous-plafond%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CConso_5_usages_%C3%A9_finale%2CConso_chauffage_%C3%A9_finale%2CConso_ECS_%C3%A9_finale%2CClasse_altitude%2CEtiquette_DPE%2CAdresse_(BAN)%2CNom__commune_(BAN)%2CCode_postal_(BAN)%2C_geopoint")

# # Récupération des données
# all_data = api.get_all_data()

# [TEMP] Récupération des données depuis un fichier CSV
all_data = pd.read_csv("data.csv")

# Création du DataFrame
df = pd.DataFrame(all_data)

# Instanciation et exécution de l'interface Dash
interface = DashInterface(df)
interface.run()