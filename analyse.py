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

culture_df = culture_df[~culture_df['Type équipement ou lieu'].isin(types_a_supprimer)]
culture_df['Type équipement ou lieu'].value_counts()

# Regroupement de certains types d'équipements ou lieux culturels similaires
types_a_regrouper = [
    'Centre de création artistique',
    'Centre d\'art',
    'Centre de création musicale',
    'Centre culturel'
]

culture_df.loc[:,'Type équipement ou lieu'] = culture_df['Type équipement ou lieu'].replace({
    'Centre de création artistique': 'Centre culturel',
    'Centre d\'art': 'Centre culturel',
    'Centre de création musicale': 'Centre culturel'
})

culture_df['Type équipement ou lieu'].value_counts()

