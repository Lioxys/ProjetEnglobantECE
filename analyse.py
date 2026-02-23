import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import requests
import os 

culture_df = pd.read_excel('ProjetEnglobantECE/Datasets/basilic.xlsx')

colonnes_a_garder = [
    'Nom',
    'Code_Postal',
    'libelle_geographique',
    'code_insee',
    'Type_equipement_ou_lieu',
    'Region',
    'Adresse_postale',
    'Departement'
]


# Affichage nombre de lignes et de colonnes, types de données et valeurs manquantes
print(f"Number of rows : {culture_df.shape[0]}")
print(f"Number of columns : {culture_df.shape[1]}")
culture_df.dtypes 

culture_df.isnull().sum().sort_values(ascending=False)

# Colonnes à garder
culture_df = culture_df[colonnes_a_garder].copy()

# Affichage des différents types d'équipements ou lieux culturels
culture_df['Type_equipement_ou_lieu'].value_counts().sort_values(ascending=False)

# Uniformisation des noms de villes par rapport à leurs arrondissements
culture_df['libelle_geographique'] = culture_df['libelle_geographique'].replace({
    r'^Paris \d+.*': 'Paris',
    r'^Lyon \d+.*': 'Lyon',
    r'^Marseille \d+.*': 'Marseille'
}, regex=True)

# Suppression des types d'équipements ou lieux culturels qui ne sont pas pertinents pour l'analyse
types_a_supprimer = [
    'Monument',
    'Papeterie et maisons de la presse',
    'Librairie',
    'Espace protégé',
    "Service d'archives",
    'Lieu archéologique',
    'Parc et jardin',
    'Lieu de mémoire',
    "Établissement d'enseignement supérieur"
]

culture_df = culture_df[~culture_df['Type_equipement_ou_lieu'].isin(types_a_supprimer)]
culture_df['Type_equipement_ou_lieu'].value_counts()

# Regroupement de certains types d'équipements ou lieux culturels similaires
types_a_regrouper = [
    'Centre de création artistique',
    'Centre d\'art',
    'Centre de création musicale',
    'Centre culturel'
]

culture_df.loc[:,'Type_equipement_ou_lieu'] = culture_df['Type_equipement_ou_lieu'].replace({
    'Centre de création artistique': 'Centre culturel',
    'Centre d\'art': 'Centre culturel',
    'Centre de création musicale': 'Centre culturel'
})

culture_df['Type_equipement_ou_lieu'].value_counts()

# Traitement du fichier de population
xls_population = pd.ExcelFile("population.xlsx")

population_df = pd.read_excel(xls_population, sheet_name=xls_population.sheet_names[0], header=5) 
population_df.shape[0]

population_df[population_df.isnull().any(axis=1)]

population_df[population_df["P18_POP"] < 0]

columns_kept = ["LIBGEO","CODGEO","P18_POP", "P18_POP0014", "P18_POP1529", "P18_POP3044", "P18_POP4559", "P18_POP6074", "P18_POP7589", "P18_POP90P"]

final_pop_df = population_df[columns_kept]

# Fusion des deux DataFrames
culture_df = culture_df.copy()

# Villes en minuscules et sans espaces pour faciliter la fusion
culture_df.loc[:, "ville_clean"] = culture_df["libelle_geographique"].str.strip().str.lower()

final_pop_df = final_pop_df.copy()
final_pop_df.loc[:, "ville_clean"] = final_pop_df["LIBGEO"].str.strip().str.lower()

# Opérations pour uniformiser les noms de villes sur les départements
culture_df.loc[culture_df["ville_clean"].str.startswith("paris"), "code_insee"] = "75000"
culture_df.loc[culture_df["ville_clean"].str.startswith("marseille"), "code_insee"] = "13000"
culture_df.loc[culture_df["ville_clean"].str.startswith("lyon"), "code_insee"] = "69000"


final_pop_df.loc[final_pop_df["ville_clean"].str.startswith("paris"), "CODGEO"] = "75000"
final_pop_df.loc[final_pop_df["ville_clean"].str.startswith("marseille"), "CODGEO"] = "13000"
final_pop_df.loc[final_pop_df["ville_clean"].str.startswith("lyon"), "CODGEO"] = "69000"

# Jointure 
culturepop = pd.merge(
    culture_df,
    final_pop_df,
    right_on=["CODGEO","ville_clean"],
    left_on=["code_insee","ville_clean"],
    how="inner"
)