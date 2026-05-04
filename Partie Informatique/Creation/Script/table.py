import sqlite3

db = sqlite3.connect("base_de_donnée.db")
curseur = db.cursor()

# Suppression des tables existantes pour repartir de zéro
curseur.execute("DROP TABLE IF EXISTS Geographiques_et_climatiques")
curseur.execute("DROP TABLE IF EXISTS Qualite_Air")
curseur.execute("DROP TABLE IF EXISTS Socio_economiques")

# 1. Création Geographiques_et_climatiques
curseur.execute("""
CREATE TABLE Geographiques_et_climatiques(
    id_Geographique_et_climatiques INTEGER PRIMARY KEY AUTOINCREMENT,
    code_insee_com TEXT,
    nom_com TEXT,
    reg_code TEXT,
    reg_nom TEXT,
    dep_code TEXT,
    dep_nom TEXT,
    population REAL,
    superficie_km2 REAL,
    densite REAL,
    latitude REAL,
    longitude REAL,
    densite_cat TEXT,
    alti_med REAL,
    RR_med REAL,
    NBJRR1_med REAL,
    NBJRR5_med REAL,
    NBJRR10_med REAL,
    Tmin_med REAL,
    Tmax_med REAL,
    Tens_vap_med REAL,
    Force_vent_med REAL,
    Insolation_med REAL,
    Rayonnement_med REAL
)
""")

# 2. Création Qualite_Air
curseur.execute("""
CREATE TABLE Qualite_Air(
    id_Qualite_aire INTEGER PRIMARY KEY AUTOINCREMENT,
    id_Geographique_et_climatiques INTEGER,
    nom_dept TEXT,
    nom_com TEXT,
    code_insee_com TEXT,
    nom_station TEXT,
    code_station TEXT,
    typologie TEXT,
    influence TEXT,
    nom_poll TEXT,
    valeur_poll REAL,
    jour INTEGER,
    mois INTEGER,
    annee INTEGER
)
""")

# 3. Création Socio_economiques (avec les noms exacts du CSV)
curseur.execute("""
CREATE TABLE Socio_economiques(
    id_Socio_economiques INTEGER PRIMARY KEY AUTOINCREMENT,
    id_Geographique_et_climatiques INTEGER,
    code_insee_com TEXT,
    nom_com TEXT,
    niveau_vie_median_2021 REAL,
    nb_logements_2022 REAL,
    Pourcentage_appartements_2022 REAL,
    pourcentage_locataires_dans_résidence_principale_2022 REAL,
    "evolution_annuelle_moy_de_la_population_entre_2017_et_ 2023_en_pourcentage" REAL,
    population_municipale_2023 REAL,
    "Taux_activite_tranche_15-64_en_2022" REAL
)
""")

db.commit()
db.close()
print("Base de données et tables créées avec succès.")