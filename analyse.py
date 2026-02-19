import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import requests
import os 

api_key = 'eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjoiNjk5NmQxNmVjNGRlMzVjYTMxMDNhMTg0IiwidGltZSI6MTc3MTQ5MTc1Ni40Mjc4MTE0fQ.MLYjGNexIinxjtlYtSwa2p0pRaYkjh2XbiQsHEXMA7KcUvPllOSFEpjcPMBu11bdcgxjy8ANqI4Wu_qGzJaXsw'
headers = {
    'content-language': 'fr-fr',
    'content-length': '33',
    'content-type': 'application/json'
}
#response = requests.get("https://equipements.sports.gouv.fr/api/explore/v2.1/catalog/datasets/data-es/records/?offset=0", headers=headers)
response2 = requests.get("https://equipements.sports.gouv.fr/api/explore/v2.1/catalog/datasets/data-es/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true&apikey=eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjoiNjk5NmQxNmVjNGRlMzVjYTMxMDNhMTg0IiwidGltZSI6MTc3MTQ5MTc1Ni40Mjc4MTE0fQ.MLYjGNexIinxjtlYtSwa2p0pRaYkjh2XbiQsHEXMA7KcUvPllOSFEpjcPMBu11bdcgxjy8ANqI4Wu_qGzJaXsw", headers=headers)
print(response2.status_code)
equipements = response.json()
equipements_df = equipements['results']


culture = pd.read_excel('ProjetEnglobant/basilic.xlsx')
revenu = pd.read_excel('ProjetEnglobant/revenuFR.xlsx')

cultureDF = culture[['Code_Postal', 'libelle_geographique', 'Type_equipement_ou_lieu', 'Region', 'Domaine', 'Sous_domaine', 'Departement', 'N_Departement', 'Latitude', 'Longitude']]
cultureDF.dropna(subset=['Code_Postal'])
filtered_cultureDF = cultureDF[cultureDF['Type_equipement_ou_lieu'].isin(['Bibliothèque', 'Centre d\'art', 'Centre de création artistique', 'Cinéma', 'Centre de création musicale', 'Théâtre', 'Conservatoire', 'Établissement d\'enseignement supérieur', 'Librairie', 'Musée', 'Opéra', 'Papeterie et maisons de la presse', 'Centre culturel'])]

revenuDF = revenu[['Nom géographique GMS', 'Code géographique', 'Libellé géographique', 'Nbre de menages fiscaux']]
revenuDF.dropna(subset=['Code géographique'])

