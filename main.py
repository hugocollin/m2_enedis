from interface import DashInterface

import pandas as pd

def main():
    """
    Fonction principale du programme
    """
    
    # Récupération des données
    df = pd.read_csv(f'assets/data_69.csv', sep='|')
    
    # Instanciation et exécution de l'interface Dash
    interface = DashInterface(df)
    interface.run()

if __name__ == "__main__":
    main()