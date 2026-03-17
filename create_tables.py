from sqlalchemy import create_engine, text

DB_URL = "mysql+pymysql://root@localhost:3306/projetenglobant"

engine = create_engine(DB_URL)

def create_tables():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS communes (
                code_insee VARCHAR(10) PRIMARY KEY,
                nom_commune VARCHAR(150),
                libelle_geographique VARCHAR(150),
                libcom VARCHAR(150),
                ville_clean VARCHAR(150),
                code_postal VARCHAR(20),
                departement VARCHAR(100),
                region VARCHAR(100)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS indicateurs_commune (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code_insee VARCHAR(10) NOT NULL,
                p18_pop INT,
                p18_pop0014 INT,
                p18_pop1529 INT,
                p18_pop3044 INT,
                p18_pop4559 INT,
                p18_pop6074 INT,
                p18_pop75p INT,
                dec_med18 DECIMAL(12,2),
                UNIQUE(code_insee),
                FOREIGN KEY (code_insee) REFERENCES communes(code_insee)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS equipements_culturels (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(255),
                type_equipement_ou_lieu VARCHAR(150),
                adresse_postale VARCHAR(255),
                code_insee VARCHAR(10) NOT NULL,
                code_postal VARCHAR(20),
                latitude DECIMAL(15, 8),
                longitude DECIMAL(15, 8),
                FOREIGN KEY (code_insee) REFERENCES communes(code_insee)
            )
        """))

    print("Tables créées avec succès.")


if __name__ == "__main__":
    create_tables()