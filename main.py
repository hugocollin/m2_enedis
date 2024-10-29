from api import API
import pandas as pd

# Instanciation de la classe avec l'URL de base
api = API("https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q={county}&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29")

# Paramètres de la requête (à changer par la suite afin de récupérer les données souhaitées)
query_params = {"county": "69"}

# Récupération des données
all_data = api.get_all_data(query_params)

# Création du DataFrame
df = pd.DataFrame(all_data)

# [TEMP] Affichage du DataFrame
print(df)