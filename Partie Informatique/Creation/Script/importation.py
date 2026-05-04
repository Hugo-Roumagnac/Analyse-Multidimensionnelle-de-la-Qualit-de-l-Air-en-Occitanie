import sqlite3
import csv

# Méthode : sqlite3.connect
# Rôle : Initialise la connexion au moteur de base de données situé dans le répertoire "Donnée".
db = sqlite3.connect("base_de_donnée.db")

# Méthode : db.cursor
# Rôle : Instancie un curseur pour l'exécution des transactions SQL.
curseur = db.cursor()

# Fonction : importer_donnees
# Rôle : Automatise la lecture, le formatage et l'insertion de données CSV dans une table SQL ciblée.
# Paramètres : 
#   - nom_fichier : chemin d'accès vers le fichier source CSV.
#   - table : nom de la table de destination dans la base de données.
def importer_donnees(nom_fichier, table):
    # Gestionnaire de contexte pour l'ouverture du fichier en lecture (mode 'r') avec encodage UTF-8.
    with open(nom_fichier, mode='r', encoding='utf-8') as file:
        # Utilisation de csv.DictReader : transforme chaque ligne du CSV en dictionnaire Python.
        # Les clés du dictionnaire correspondent aux en-têtes du fichier CSV.
        reader = csv.DictReader(file)
        
        for row in reader:
            # Traitement dynamique des colonnes : 
            # Les noms des colonnes sont encapsulés dans des doubles guillemets pour prévenir les erreurs
            # de syntaxe liées aux caractères spéciaux (espaces, tirets, accents).
            colonnes = ', '.join([f'"{col}"' for col in row.keys()])
            
            # Préparation des marqueurs de substitution (placeholders) "?" pour sécuriser l'insertion
            # et prévenir les injections SQL.
            placeholders = ', '.join(['?'] * len(row))
            
            # Méthode : Construction de la requête SQL de type INSERT INTO.
            sql = f'INSERT INTO {table} ({colonnes}) VALUES ({placeholders})'
            
            # Exécution de la requête avec passage des valeurs sous forme de tuple.
            curseur.execute(sql, tuple(row.values()))
            
    # Méthode : db.commit
    # Rôle : Validation groupée de toutes les transactions d'insertion pour le fichier en cours.
    db.commit()
    print(f"Importation terminée pour {table}")

# Bloc : Exécution séquentielle des flux de données
# Chaque appel traite un fichier source distinct vers sa table respective.

# Import des données géographiques et climatiques
importer_donnees('Creation/Donnée/donnees_geo_climatiques.csv', 'Geographiques_et_climatiques')

# Import des mesures de qualité de l'air (données journalières)
importer_donnees('Creation/Donnée/mesures_occitanie_journaliere_pollution.csv', 'Qualite_Air')

# Import des indicateurs socio-économiques
importer_donnees('Creation/Donnée/donnees_socio_economiques.csv', 'Socio_economiques')

# Méthode : db.close
# Rôle : Fermeture de la connexion pour libérer les accès au fichier de base de données.
db.close()
print("\n")