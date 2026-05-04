import sqlite3
import math
import csv
from exporter_donnees.Script.export_csv import exporter_en_csv

def calcul_moyenne(liste):
    """Calcule la moyenne arithmétique d'une liste de valeurs numériques."""
    return sum(liste) / len(liste) if liste else 0

def noel():
    """
    Analyse l'impact des fêtes de fin d'année sur la pollution atmosphérique (NOX).
    Compare les niveaux de pollution entre une période "normale" et la période de Noël/Nouvel An.
    """
    # Connexion à la base de données SQLite
    db = sqlite3.connect("base_de_donnée.db")
    cur = db.cursor()
    
    # 1. PRÉPARATION DES DONNÉES VIA UNE VUE SQL
    # Nettoyage de la vue existante pour permettre la réexécution du script
    cur.execute("DROP VIEW IF EXISTS comparatif_noel")
    
    # Création d'une vue pour isoler deux périodes distinctes par commune :
    # - Moyenne_Noel : du 20 décembre au 5 janvier (fêtes)
    # - Moyenne_Normal : du 5 au 19 décembre (référence pré-fêtes)
    # Filtre sur les stations 'Urbaines' liées au 'Trafic' pour isoler l'activité humaine.
    cur.execute("""
        CREATE VIEW comparatif_noel AS
        SELECT 
            nom_com AS Commune,
            AVG(CASE WHEN (annee = 2022 AND mois = 12 AND jour >= 20) 
                       OR (annee = 2023 AND mois = 1 AND jour <= 5) 
                THEN valeur_poll END) AS Moyenne_Noel,
            AVG(CASE WHEN (annee = 2022 AND mois = 12 AND jour BETWEEN 5 AND 19) 
                THEN valeur_poll END) AS Moyenne_Normal
        FROM Qualite_Air
        WHERE nom_poll = 'NOX' AND typologie = 'Urbaine' AND influence = 'Trafic'
        GROUP BY nom_com
        HAVING Moyenne_Noel IS NOT NULL AND Moyenne_Normal IS NOT NULL;
    """)
    
    # Extraction des données calculées
    res = cur.execute("SELECT * FROM comparatif_noel").fetchall()

    # 2. TRAITEMENT ET CALCULS STATISTIQUES
    # Organisation des données en listes pour le traitement Python
    villes = [row[0] for row in res]
    noel_vals = [row[1] for row in res]
    normal_vals = [row[2] for row in res]
    
    # Calcul des moyennes globales des deux périodes
    m_noel = calcul_moyenne(noel_vals)
    m_normal = calcul_moyenne(normal_vals)

    # Initialisation des accumulateurs pour le calcul du coefficient de Pearson (r)
    num = 0
    den_noel = 0
    den_normal = 0
    lignes_stats = []
    
    # Calcul manuel de la corrélation et préparation des lignes détaillées
    for i in range(len(villes)):
        dx = normal_vals[i] - m_normal # Écart à la moyenne (Normal)
        dy = noel_vals[i] - m_noel     # Écart à la moyenne (Noël)
        
        num += dx * dy
        den_noel += dx**2
        den_normal += dy**2
        
        lignes_stats.append([villes[i], round(normal_vals[i],2), round(noel_vals[i],2), round(dx,2), round(dy,2)])

    # Formule finale du coefficient de corrélation
    r = num / math.sqrt(den_noel * den_normal) if den_noel * den_normal != 0 else 0

    # 3. AFFICHAGE DANS LE TERMINAL
    print(f"\n ANALYSE COMPARATIVE : PÉRIODE DE NOËL \n")
    print(f"{'Ville':<20} | {'Moy. Normale':<15} | {'Moy. Noël':<15}")
    for ligne in lignes_stats:
        print(f"{ligne[0]:<20} | {ligne[1]:<15.2f} | {ligne[2]:<15.2f}")
    
    print(f"MOYENNE GLOBALE NORMALE : {m_normal:.2f} µg/m³")
    print(f"MOYENNE GLOBALE NOËL    : {m_noel:.2f} µg/m³")
    print(f"COEFFICIENT DE PEARSON (r) : {r:.4f}")

    # 4. EXPORTATION DES RÉSULTATS
    
    # Export de la vue SQL brute
    exporter_en_csv(cur, "comparatif_noel", "Problematique_4/Exportation/etude_noel.csv")
    
    # Export du rapport statistique détaillé
    with open("Problematique_4/Exportation/outil_statistique_pearson.csv", mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Ville", "Pollution_Normal", "Pollution_Noel", "Ecart_Normal", "Ecart_Noel"])
        writer.writerows(lignes_stats)
        writer.writerow([])
        writer.writerow(["Coefficient de Corrélation r", round(r, 4)])

    db.close()

if __name__ == "__main__":
    noel()