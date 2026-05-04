# Analyse Multidimensionnelle de la Qualité de l'Air en Occitanie

> Projet universitaire réalisé dans le cadre de l'**UE 403 – Projet Info/Stat**  
> Licence 2 MIASHS — Université Paul Sabatier / Toulouse

---

## Membres du groupe

| Étudiant | Participation |
|---|---|
| Aït Mahammed Salim | 50 % |
| Roumagnac Hugo | 50 % |

---

## Description du projet

Ce projet analyse la **qualité de l'air en Occitanie** en combinant une approche informatique (construction d'une base de données relationnelle) et une approche statistique (analyse descriptive univariée et bivariée).

À partir de trois fichiers CSV fournis — données de **pollution atmosphérique**, **géographiques/climatiques** et **socio-économiques** — le groupe a :

1. Construit une **base de données relationnelle** avec Python et SQLite3
2. Extrait des tables pertinentes via des **requêtes SQL**
3. Conduit une **étude statistique descriptive** en répondant à quatre problématiques

---

## Structure du dépôt

```
projet/
│
├── Donnée/
│   ├── mesure_Occitanie_journaliere_pollution.csv
│   ├── données_géographiques_climatiques.csv
│   └── données_socio_économiques.csv
│
├── Scripts/
│   ├── importation.py        # Remplit les tables SQLite via les CSV
│   ├── doublon.py            # Détection et gestion des doublons
│   └── extraction.py         # Génère les fichiers CSV pour l'analyse R
│
├── Problematique_1/
│   ├── Problematique_1.Rmd
│   ├── Problematique_1.html
│   └── inf.csv
│
├── Problematique_2/
│   ├── Problematique_2.Rmd
│   ├── Problematique_2.html
│   ├── stats_hiver.csv
│   ├── stats_ete.csv
│   └── diagramme_activité_2.png
│
├── Problematique_3/
│   ├── Problematique_3.Rmd
│   ├── Problematique_3.html
│   ├── donnees_brutes_nox_urbain.csv
│   ├── indicateurs_stats_urbain.csv
│   └── diagramme_activite_3.png
│
├── Problematique_4/
│   ├── Problematique_4.Rmd
│   ├── Problematique_4.html
│   ├── outil_statistique_pearson.csv
│   └── diagramme_activite_4.png
│
├── Sommaire.Rmd              # Rapport principal (point d'entrée)
├── Sommaire.html             # Rapport compilé
└── main.py                   # Programme principal
```

---

## Problématiques étudiées

### Problématique 1 — Impact du niveau de vie sur la qualité de l'air
Analyse de la relation entre le niveau de vie médian des communes (seuil : 21 500 €) et les concentrations de **PM2.5** en milieu urbain (année 2022), à partir d'une jointure entre les tables `QUALITE_AIR` et `SOCIO_ECONOMIQUES`.

### Problématique 2 — Disparités saisonnières des concentrations de polluants
Comparaison des concentrations d'**Ozone (O3)** entre l'hiver et l'été en milieu urbain pour l'année 2023. L'O3 est retenu comme indicateur privilégié en raison de sa forte sensibilité au rayonnement solaire et aux températures.

### Problématique 3 — Impact de la densité démographique sur la qualité de l'air
Étude de la corrélation entre la densité de population et les concentrations d'**Oxydes d'Azote (NOX)** en zone urbaine (année 2022). Les NOX sont choisis pour leur lien direct avec les activités de combustion (transports, chauffage).

### Problématique 4 — Impact des fêtes de fin d'année sur la qualité de l'air
Comparaison des niveaux de pollution entre la routine de décembre et la période des vacances de fin d'année, via une vue SQL `comparatif_noel`, pour mesurer l'effet des pics d'activité festive sur les concentrations de polluants.

---

## Stack technique

| Outil | Usage |
|---|---|
| **Python 3** + `sqlite3` | Construction et gestion de la base de données |
| **SQL** | Extraction et filtrage des données |
| **R** + **RStudio** | Analyses statistiques descriptives |
| **R Markdown** | Rédaction du rapport final |
| **PowerPoint** | Présentation orale à mi-parcours + diagramme de Gantt |

---

## Lancer le projet

### 1. Construction de la base de données

```bash
python main.py
```

Ce script exécute dans l'ordre : importation des CSV, gestion des doublons, puis extraction des tables pour R.

### 2. Compilation du rapport R Markdown

Ouvrir `Sommaire.Rmd` dans **RStudio**, puis cliquer sur **Knit** (ou exécuter) :

```r
rmarkdown::render("Sommaire.Rmd")
```

Pour compiler une problématique individuellement :

```r
rmarkdown::render("Problematique_1/Problematique_1.Rmd")
```

---

## Données sources

Trois fichiers CSV fournis dans le cadre de l'UE 403 (disponibles sur IRIS) :

- `mesure_Occitanie_journaliere_pollution.csv` — Qualité de l'air en Occitanie
- Fichier géographique et climatique
- Fichier socio-économique

> Un fichier HTML *Descriptif des données* accompagne ces sources et est indispensable à la compréhension des variables.

---

## Évaluation

| Livrable | Pondération |
|---|---|
| Présentation orale à mi-parcours (6 min, 6 slides + Gantt) | 50 % |
| Rapport final R Markdown (remis le **17 avril**) | 50 % |

---

## Contexte académique

- **Formation** : L2 MIASHS
- **UE** : UE 403 — Projet Info/Stat
- **Durée** : 11 séances de travail
- **Thématique** : Pollution de l'air en Occitanie
