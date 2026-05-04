import sqlite3
import statistics
from exporter_donnees.Script.export_csv import exporter_en_csv

def niveau_de_vie():
    """
    Assure l'extraction, le traitement statistique et l'exportation des données
    de pollution atmosphérique en fonction du niveau de vie médian.
    """
    
    # Établissement de la connexion à la base de données SQLite
    db = sqlite3.connect("base_de_donnée.db")
    cur = db.cursor()

    # Nettoyage de l'espace de travail : suppression des vues préexistantes
    cur.execute("DROP VIEW IF EXISTS Ville_sup")
    cur.execute("DROP VIEW IF EXISTS Ville_inf")

    # Création de la Vue : Ville_sup
    # Regroupe les communes dont le niveau de vie est supérieur ou égal au seuil (21500€)
    # Filtres appliqués : Particules fines PM2.5, année 2022, stations de fond en milieu urbain
    cur.execute("""
    CREATE VIEW Ville_sup AS
    SELECT Q.nom_com, Q.code_insee_com, AVG(Q.valeur_poll) AS moyenne_pollution, S.niveau_vie_median_2021
    FROM Qualite_Air Q
    JOIN Socio_economiques S ON Q.code_insee_com = S.code_insee_com
    WHERE S.niveau_vie_median_2021 >= 21500
      AND Q.nom_poll = 'PM2.5' AND Q.annee = 2022
      AND influence = 'Fond' 
      AND typologie = 'Urbaine'
    GROUP BY Q.code_insee_com;
    """)

    # Création de la Vue : Ville_inf
    # Regroupe les communes dont le niveau de vie est inférieur au seuil (hors valeurs nulles)
    # Les critères de pollution restent identiques pour permettre la comparaison
    cur.execute("""
    CREATE VIEW Ville_inf AS
    SELECT Q.nom_com, Q.code_insee_com, AVG(Q.valeur_poll) AS moyenne_pollution, S.niveau_vie_median_2021
    FROM Qualite_Air Q
    JOIN Socio_economiques S ON Q.code_insee_com = S.code_insee_com
    WHERE S.niveau_vie_median_2021 < 21500
      AND S.niveau_vie_median_2021 > 0
      AND Q.nom_poll = 'PM2.5' AND Q.annee = 2022
      AND influence = 'Fond'              
      AND typologie = 'Urbaine'
    GROUP BY Q.code_insee_com;
    """)

    
    def etude_univariee():
        
        #Calcule et affiche les indicateurs de tendance centrale et de dispersion
        #pour chaque groupe de communes afin d'étudier la distribution de la pollution.
        
        print(f"\n ÉTUDE UNIVARIÉE DES GROUPES (Seuil : 21500€)\n")
        
        for vue in ["Ville_inf", "Ville_sup"]:
            # Récupération des moyennes de pollution calculées dans les vues SQL
            cur.execute(f"SELECT moyenne_pollution FROM {vue}")
            donnees = [r[0] for r in cur.fetchall()]
            
            if donnees:
                print(f"\nANALYSE DU GROUPE : {vue}\n")
                print(f"Effectif          : {len(donnees)} villes")
                print(f"Moyenne           : {statistics.mean(donnees):.2f} µg/m³")
                print(f"Médiane           : {statistics.median(donnees):.2f} µg/m³")
                # Calcul de l'écart-type si l'échantillon comporte au moins deux points de données
                if len(donnees) > 1:
                    print(f"Écart-type        : {statistics.stdev(donnees):.2f}")

    # Exécution de l'analyse statistique descriptive
    etude_univariee()
    
    # Exportation des résultats vers des fichiers CSV pour traitement ultérieur (graphiques)
    exporter_en_csv(cur, "Ville_inf", "Problematique_1/Exportation/inf.csv")
    exporter_en_csv(cur, "Ville_sup", "Problematique_1/Exportation/sup.csv")

    # Fermeture de la connexion à la base de données
    db.close()

if __name__ == "__main__":
    niveau_de_vie()