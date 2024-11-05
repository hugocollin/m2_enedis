from interface import DashInterface

import pandas as pd

def main():
    """
    Fonction principale du programme
    """
    
    # Récupération des données
    df = pd.read_csv(f'data/data_69.csv', sep='|')

    # # [TEMP] Entraînement du modèle 
    # from model import Model
    # Model.train(df, local_data=True, county=69)
    
    # Instanciation et exécution de l'interface Dash
    interface = DashInterface(df)
    interface.run()

if __name__ == "__main__":
    main()