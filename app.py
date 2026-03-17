from fastapi import FastAPI, Query
from sqlalchemy import create_engine
import pandas as pd

DB_URL = "mysql+pymysql://root@localhost:3306/projetenglobant"
engine = create_engine(DB_URL)

app = FastAPI(title="API Projet Englobant", version="1.0")


@app.get("/")
def home():
    return {"message": "API Projet Englobant active"}


@app.get("/communes")
def get_communes(limit: int = Query(default=100, le=1000)):
    query = """
        SELECT *
        FROM communes
        LIMIT %(limit)s
    """
    df = pd.read_sql(query, engine, params={"limit": limit})
    return df.to_dict(orient="records")


@app.get("/communes/{code_insee}")
def get_commune(code_insee: str):
    query = """
        SELECT *
        FROM communes
        WHERE code_insee = %(code_insee)s
    """
    df = pd.read_sql(query, engine, params={"code_insee": code_insee})
    return df.to_dict(orient="records")


@app.get("/communes/{code_insee}/indicateurs")
def get_indicateurs_commune(code_insee: str):
    query = """
        SELECT *
        FROM indicateurs_commune
        WHERE code_insee = %(code_insee)s
    """
    df = pd.read_sql(query, engine, params={"code_insee": code_insee})
    return df.to_dict(orient="records")


@app.get("/communes/{code_insee}/equipements")
def get_equipements_commune(code_insee: str):
    query = """
        SELECT id, nom, type_equipement_ou_lieu, adresse_postale, code_postal
        FROM equipements_culturels
        WHERE code_insee = %(code_insee)s
    """
    df = pd.read_sql(query, engine, params={"code_insee": code_insee})
    return df.to_dict(orient="records")


@app.get("/equipements")
def get_equipements(limit: int = Query(default=100, le=1000)):
    query = """
        SELECT *
        FROM equipements_culturels
        LIMIT %(limit)s
    """
    df = pd.read_sql(query, engine, params={"limit": limit})
    return df.to_dict(orient="records")


@app.get("/indicateurs/top-equipements")
def top_equipements(limit: int = Query(default=20, le=100)):
    query = """
        SELECT 
            c.code_insee,
            c.nom_commune,
            c.region,
            COUNT(e.id) AS nb_equipements
        FROM communes c
        LEFT JOIN equipements_culturels e
            ON c.code_insee = e.code_insee
        GROUP BY c.code_insee, c.nom_commune, c.region
        ORDER BY nb_equipements DESC
        LIMIT %(limit)s
    """
    df = pd.read_sql(query, engine, params={"limit": limit})
    return df.to_dict(orient="records")


@app.get("/indicateurs/ratio-equipements-population")
def ratio_equipements_population(limit: int = Query(default=20, le=100)):
    query = """
        SELECT 
            c.code_insee,
            c.nom_commune,
            i.p18_pop,
            COUNT(e.id) AS nb_equipements,
            CASE
                WHEN i.p18_pop > 0 THEN ROUND(COUNT(e.id) * 10000.0 / i.p18_pop, 2)
                ELSE NULL
            END AS ratio_pour_10000_hab
        FROM communes c
        JOIN indicateurs_commune i
            ON c.code_insee = i.code_insee
        LEFT JOIN equipements_culturels e
            ON c.code_insee = e.code_insee
        GROUP BY c.code_insee, c.nom_commune, i.p18_pop
        ORDER BY ratio_pour_10000_hab DESC
        LIMIT %(limit)s
    """
    df = pd.read_sql(query, engine, params={"limit": limit})
    return df.to_dict(orient="records")


@app.get("/recherche/communes")
def search_communes(nom: str):
    query = """
        SELECT *
        FROM communes
        WHERE nom_commune LIKE %(nom)s
           OR libelle_geographique LIKE %(nom)s
           OR libcom LIKE %(nom)s
    """
    df = pd.read_sql(query, engine, params={"nom": f"%{nom}%"})
    return df.to_dict(orient="records")