import csv

def exporter_en_csv(cur, nom_source, nom_fichier):
    
    #Exporte le contenu d'une table ou d'une vue SQLite vers un fichier CSV.
    #nom_source : nom de la table ou de la vue
    
    cur.execute(f"SELECT * FROM {nom_source}")
    lignes = cur.fetchall()
    entetes = [description[0] for description in cur.description]
    
    if lignes:
        with open(nom_fichier, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(entetes)
            writer.writerows(lignes)  # <--- AJOUTE CETTE LIGNE (écrit tout le contenu)
