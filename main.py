from interface import DashInterface

import pandas as pd

def main(county):
    """
    Fonction principale du programme
    """
    
    # Récupération des données
    df = pd.read_csv(f'data/data_{county}.csv', sep='|')
    
    # Instanciation et exécution de l'interface Dash
    interface = DashInterface(df, county)
    interface.run()

if __name__ == "__main__":
    main(county='69')