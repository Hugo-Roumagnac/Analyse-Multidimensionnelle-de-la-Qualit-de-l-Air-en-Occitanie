import sqlite3
import statistics
from exporter_donnees.Script.export_csv import exporter_en_csv

def saisons():
    """
    Analyse de la dynamique saisonnière de l'Ozone (O3) à Toulouse pour l'année 2023.
    Cette fonction génère des statistiques descriptives (moyennes, écart-types) 
    et exporte les résultats pour une exploitation ultérieure sous R.
    """
    
    # Connexion à la base de données SQLite
    db = sqlite3.connect("base_de_donnée.db")
    cur = db.cursor()

    # --- ÉTAPE 1 : CRÉATION DE LA VUE GLOBALE (PIVOT MENSUEL) ---
    # On prépare dynamiquement la requête SQL pour calculer la moyenne de chaque mois
    mois_noms_cols = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", 
                      "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
    
    # Génération des clauses AVG(CASE...) pour transformer les lignes en colonnes (Pivot)
    mois_sql = ", ".join([f"AVG(CASE WHEN mois={m} THEN valeur_poll END) AS {mois_noms_cols[m-1]}" for m in range(1, 13)])
    
    cur.execute("DROP VIEW IF EXISTS Vue_Qualite_Air_Ozone")
    cur.execute(f"""
    CREATE VIEW Vue_Qualite_Air_Ozone AS
    SELECT 
        'TOULOUSE' AS Ville,
        'URBAINE' AS Typologie,
        'FOND' AS Influence,
        2023 AS Annee,
        {mois_sql},
        -- Agrégation par saison (Moyenne brute des relevés de la période)
        AVG(CASE WHEN mois IN (12,1,2) THEN valeur_poll END) AS Hiver,
        AVG(CASE WHEN mois IN (3,4,5)  THEN valeur_poll END) AS Printemps,
        AVG(CASE WHEN mois IN (6,7,8)  THEN valeur_poll END) AS Ete,
        AVG(CASE WHEN mois IN (9,10,11) THEN valeur_poll END) AS Automne
    FROM Qualite_Air 
    WHERE annee = 2023 
      AND (nom_poll LIKE '%O3%' OR nom_poll LIKE '%OZONE%')
      AND Typologie = 'Urbaine' AND Influence = 'Fond'
      AND nom_com = 'TOULOUSE'
    GROUP BY 1, 2, 3, 4
    """)

    # --- ÉTAPE 2 : CRÉATION DES VUES STATISTIQUES (POUR EXPORT CSV) ---
    # Utilisation de CTE pour garantir la précision mathématique
    for saison_nom, mois_tuple in [("Hiver", (12, 1, 2)), ("Ete", (6, 7, 8))]:
        cur.execute(f"DROP VIEW IF EXISTS Vue_Stats_{saison_nom}")
        cur.execute(f"""
        CREATE VIEW Vue_Stats_{saison_nom} AS
        WITH Moyennes_Mensuelles AS (
            -- Calcul de la moyenne pour chaque mois individuellement
            SELECT mois, AVG(valeur_poll) as moy_m
            FROM Qualite_Air
            WHERE annee = 2023 AND mois IN {mois_tuple}
              AND (nom_poll LIKE '%O3%' OR nom_poll LIKE '%OZONE%')
              AND Typologie = 'Urbaine' AND nom_com = 'TOULOUSE'
            GROUP BY mois
        ),
        Stats_Globales AS (
            -- Calcul de l'écart-type sur l'ensemble des relevés de la saison (volatilité réelle)
            SELECT 
                SQRT(AVG(valeur_poll*valeur_poll) - (AVG(valeur_poll)*AVG(valeur_poll))) as stdev_brute
            FROM Qualite_Air
            WHERE annee = 2023 AND mois IN {mois_tuple}
              AND (nom_poll LIKE '%O3%' OR nom_poll LIKE '%OZONE%')
              AND Typologie = 'Urbaine' AND nom_com = 'TOULOUSE' AND valeur_poll IS NOT NULL
        )
        SELECT 
            'TOULOUSE' AS Ville,
            'URBAINE' AS Typologie,
            'FOND' AS Influence,
            2023 AS Annee,
            -- La "Moyenne des Moyennes" : on donne le même poids à chaque mois
            (SELECT AVG(moy_m) FROM Moyennes_Mensuelles) AS Moyenne,
            (SELECT stdev_brute FROM Stats_Globales) AS Ecart_Type
        """)

    # --- ÉTAPE 3 : AFFICHAGE DES RÉSULTATS DANS LE TERMINAL ---
    res = cur.execute("SELECT * FROM Vue_Qualite_Air_Ozone").fetchall()
    
    if res:
        mois_noms = ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
        saisons_liste = ["Hiver", "Printemps", "Été", "Automne"]
        
        for row in res:
            print(f"\n RÉSULTATS ANALYSE : {row[0]} ({row[3]}) ")
            print(f" CONFIGURATION : {row[1]} / {row[2]}")
            
            print("\n[Moyennes Mensuelles]")
            for i, m in enumerate(mois_noms):
                # row[i+4] car les 4 premières colonnes sont Ville, Typo, Influence, Annee
                print(f"  {m:<10} : {row[i+4] or 0:>6.2f} µg/m³")
            
            print("\n[Moyennes Saisonnières]")
            for i, s in enumerate(saisons_liste):
                # row[i+16] correspond aux colonnes saisonnières calculées
                print(f"  {s:<10} : {row[i+16] or 0:>6.2f} µg/m³")

            # Calcul de l'écart-type via le module statistics de Python pour vérification
            print("\n[Indices de Dispersion]")
            for nom, mois in [("HIVER", (12,1,2)), ("ÉTÉ", (6,7,8))]:
                cur.execute(f"SELECT valeur_poll FROM Qualite_Air WHERE annee=2023 AND mois IN {mois} AND nom_com='TOULOUSE' AND valeur_poll IS NOT NULL")
                data = [r[0] for r in cur.fetchall()]
                if len(data) > 1:
                    print(f"  Écart-type {nom} : {statistics.stdev(data):.2f}")

    # --- ÉTAPE 4 : EXPORTATION DES DONNÉES ---
    # Export de la vue globale 
    exporter_en_csv(cur, "Vue_Qualite_Air_Ozone", "Problematique_2/Exportation/ozone_saisons_2023.csv")
    
    # Export des statistiques résumées pour l'Hiver et l'Été
    exporter_en_csv(cur, "Vue_Stats_Hiver", "Problematique_2/Exportation/stats_hiver.csv")
    exporter_en_csv(cur, "Vue_Stats_Ete", "Problematique_2/Exportation/stats_ete.csv")
    
    db.close()

if __name__ == '__main__':
    saisons()