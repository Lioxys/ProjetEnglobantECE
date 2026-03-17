import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = "mysql+pymysql://root@localhost:3306/projetenglobant"
CSV_PATH = "Datasets/full_df.csv"

engine = create_engine(DB_URL)


def load_csv(path=CSV_PATH):
    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    text_cols = [
        "Nom", "Code_Postal", "libelle_geographique", "code_insee",
        "Type_equipement_ou_lieu", "Region", "Adresse_postale",
        "Departement", "ville_clean", "LIBCOM", "Latitude", "Longitude"
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    numeric_cols = [
        "P18_POP", "P18_POP0014", "P18_POP1529", "P18_POP3044",
        "P18_POP4559", "P18_POP6074", "P18_POP75P", "DEC_MED18", "Latitude", "Longitude"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["code_insee"]).copy()

    return df


def build_communes_df(df):
    communes_df = df[[
        "code_insee", "libelle_geographique", "LIBCOM", "ville_clean",
        "Code_Postal", "Departement", "Region"
    ]].copy()

    communes_df = communes_df.rename(columns={
        "LIBCOM": "libcom",
        "Code_Postal": "code_postal",
        "Departement": "departement",
        "Region": "region"
    })

    communes_df["nom_commune"] = communes_df["libelle_geographique"]

    communes_df = communes_df[[
        "code_insee", "nom_commune", "libelle_geographique",
        "libcom", "ville_clean", "code_postal", "departement", "region"
    ]]

    communes_df = communes_df.drop_duplicates(subset=["code_insee"])

    return communes_df


def build_indicateurs_df(df):
    indicateurs_df = df[[
        "code_insee", "P18_POP", "P18_POP0014", "P18_POP1529",
        "P18_POP3044", "P18_POP4559", "P18_POP6074", "P18_POP75P",
        "DEC_MED18"
    ]].copy()

    indicateurs_df = indicateurs_df.rename(columns={
        "P18_POP": "p18_pop",
        "P18_POP0014": "p18_pop0014",
        "P18_POP1529": "p18_pop1529",
        "P18_POP3044": "p18_pop3044",
        "P18_POP4559": "p18_pop4559",
        "P18_POP6074": "p18_pop6074",
        "P18_POP75P": "p18_pop75p",
        "DEC_MED18": "dec_med18"
    })

    indicateurs_df = indicateurs_df.drop_duplicates(subset=["code_insee"])

    return indicateurs_df


def build_equipements_df(df):
    equipements_df = df[[
        "Nom", "Type_equipement_ou_lieu", "Adresse_postale",
        "code_insee", "Code_Postal", "Latitude", "Longitude"
    ]].copy()

    equipements_df = equipements_df.rename(columns={
        "Nom": "nom",
        "Type_equipement_ou_lieu": "type_equipement_ou_lieu",
        "Adresse_postale": "adresse_postale",
        "Code_Postal": "code_postal"
    })

    equipements_df = equipements_df.drop_duplicates()

    return equipements_df


def clear_tables():
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("TRUNCATE TABLE equipements_culturels"))
        conn.execute(text("TRUNCATE TABLE indicateurs_commune"))
        conn.execute(text("TRUNCATE TABLE communes"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


def load_to_mysql():
    df = load_csv(CSV_PATH)

    communes_df = build_communes_df(df)
    indicateurs_df = build_indicateurs_df(df)
    equipements_df = build_equipements_df(df)

    clear_tables()

    communes_df.to_sql("communes", con=engine, if_exists="append", index=False)
    indicateurs_df.to_sql("indicateurs_commune", con=engine, if_exists="append", index=False)
    equipements_df.to_sql("equipements_culturels", con=engine, if_exists="append", index=False)

    print("Ingestion terminée.")
    print(f"Communes : {len(communes_df)}")
    print(f"Indicateurs : {len(indicateurs_df)}")
    print(f"Équipements : {len(equipements_df)}")


if __name__ == "__main__":
    load_to_mysql()