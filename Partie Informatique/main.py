# FICHIER PRINCIPAL (MAIN.PY) : GESTIONNAIRE DE PROJET
# Ce script sert de point d'entrée unique. Il centralise la logique
# du projet en appelant des modules spécialisés pour chaque tâche.

try:
    # Importation des scripts de gestion de la base de données 
    import Creation.Script.table as table          
    import Creation.Script.importation as impt     
    
    # Importation des modules d'analyses (Problématiques)
    # L'utilisation d'alias (p1, p2...) facilite l'appel des fonctions
    import Problematique_1.Script.extraction as p1
    import Problematique_2.Script.saisons as p2
    import Problematique_3.Script.population as p3
    import Problematique_4.Script.noel as p4

except ImportError as e:
    # Sécurité : Empêche le programme de planter si un fichier est manquant
    print(f"Erreur lors du chargement des modules : {e}")

def initialiser_bd():
    
    #Procédure d'initialisation (Pipeline ETL) :
    #1. Crée la structure des tables SQL.
    #2. Nettoie et importe les données brutes des fichiers sources.
    
    print("\n  Initialisation de la Base de Données ")
    table.creer_tables()    
    impt.importer_donnees() 
    print("  Fin de l'initialisation \n")

def menu():
    
    #Interface Utilisateur (CLI) :
    #Permet de piloter le projet sans modifier le code source.
    
    # Option de réinitialisation : utile pour le développement et la correction
    init = input(" Voulez-vous réinitialiser la base de données (O/N) ? : ").strip().upper()
    if init == 'O':
        initialiser_bd()

    # Boucle de navigation infinie jusqu'à ce que l'utilisateur choisisse de quitter (0)
    while True:
        print("   \n\nMENU PROJET STATISTIQUE\n")
        print("1. Problématique 1 : Analyse Niveau de Vie")
        print("2. Problématique 2 : Analyse Saisonnière (O3)")
        print("3. Problématique 3 : Corrélation Spatiale & Population")
        print("4. Problématique 4 : Modélisation / Prévisions")
        print("0. Quitter")
        
        choix = input("\n Votre choix : ").strip().upper()

        # Routage vers les fonctions spécifiques de chaque problématique
        if choix == '1':
            p1.niveau_de_vie() 
        elif choix == '2':
            p2.saisons() 
        elif choix == '3':
            p3.densite_population()    
        elif choix == '4':
            p4.noel()  
        elif choix == '0':
            print("Fermeture du programme. Au revoir !")
            break
        else:
            # Gestion des erreurs de saisie utilisateur
            print("Option invalide, veuillez réessayer.")

# Point d'entrée standard de Python : garantit que le menu ne se lance 
# que si ce fichier est exécuté directement (et non importé ailleurs).
if __name__ == "__main__":
    menu()