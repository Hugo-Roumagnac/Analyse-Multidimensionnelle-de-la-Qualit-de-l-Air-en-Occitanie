import sqlite3
import statistics
import csv
from exporter_donnees.Script.export_csv import exporter_en_csv

def densite_population():
    """
    Analyse la corrélation entre la densité de population et les niveaux de NOX 
    pour l'année 2022, spécifiquement pour les stations 'Urbain de fond'.
    """
    db = sqlite3.connect("base_de_donnée.db")
    cur = db.cursor()
    
    cur.execute("DROP VIEW IF EXISTS densite_population")
    
    # Création de la vue avec le filtre spécifique
    # On utilise UPPER() pour éviter les problèmes de casse (majuscules/minuscules)
    cur.execute("""
        CREATE VIEW densite_population AS
        SELECT    
            Q.nom_com AS Commune, 
            G.densite AS Densite_Valeur, 
            G.densite_cat AS Categorie,
            AVG(Q.valeur_poll) AS Moyenne_NOX, 
            Q.code_insee_com AS Code_INSEE
        FROM Qualite_Air AS Q
        JOIN Geographiques_et_climatiques AS G ON Q.code_insee_com = G.code_insee_com
        WHERE Q.annee = 2022 
          AND Q.nom_poll = 'NOX'
          AND Q.typologie = 'Urbaine'     
          AND Q.influence = 'Fond'      
        GROUP BY Q.code_insee_com;
    """)

    # Récupération des données triées
    res = cur.execute("SELECT * FROM densite_population ORDER BY Densite_Valeur DESC").fetchall()
    
    # Extraction des listes pour les calculs (row[3] = NOX, row[1] = Densité)
    nox = [row[3] for row in res if row[3] is not None]
    densite = [row[1] for row in res if row[1] is not None]

    # --- CALCULS STATISTIQUES ---
    moy = statistics.mean(nox)
    med = statistics.median(nox)
    ect = statistics.stdev(nox) if len(nox) > 1 else 0
    
    # Corrélation de Pearson
    # On s'assure d'avoir au moins deux points pour corréler
    if len(nox) > 1:
        mu_x, mu_y = statistics.mean(densite), statistics.mean(nox)
        num = sum((xi - mu_x) * (yi - mu_y) for xi, yi in zip(densite, nox))
        den = (sum((xi - mu_x)**2 for xi in densite) * sum((yi - mu_y)**2 for yi in nox))**0.5
        correl = num / den if den != 0 else 0
    else:
        correl = 0

    # Affichage des résultats
    print(f" SYNTHÈSE : URBAIN DE FOND (2022) ")
    print(f"Nombre de communes : {len(res)}")
    print(f"Moyenne NOX        : {moy:.2f} µg/m³") 
    print(f"Corrélation Pearson : {correl:.3f}")

    # --- EXPORTATION ---
    # Sauvegarde des indicateurs
    with open("Problematique_3/Exportation/indicateurs_stats_urbain.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['indicateur', 'valeur'])
        writer.writerow(['moyenne', round(moy, 2)])
        writer.writerow(['mediane', round(med, 2)])
        writer.writerow(['ecart_type', round(ect, 2)])
        writer.writerow(['correlation_pearson', round(correl, 3)])

    # Exportation des données brutes via ton module externe
    exporter_en_csv(cur, "densite_population", "Problematique_3/Exportation/donnees_brutes_nox_urbain.csv")
    
    db.close()

if __name__ == "__main__":
    densite_population()