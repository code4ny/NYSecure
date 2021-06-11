import psycopg2
import csv

DATABASE_URI = "postgres://kqejfycmueuecf:717cac44aaa9c449627083c73a063dab2f7a7cf7083ee18235537f651af4ad9d@ec2-50-19-176-236.compute-1.amazonaws.com:5432/df64s3e5darhft"


def get_connection():
    return psycopg2.connect(DATABASE_URI)


def read_files_to_db(fp):
    with open(fp, "r", newline="") as f:
        rows = csv.reader(f)
        header = next(rows)
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""ALTER SEQUENCE location_id_seq RESTART;""")
            cur.executemany(
                """
                INSERT INTO Location (LocationName, Block, Level) 
                VALUES (%s, %s, %s)
                """,
                rows,
            )
            cur.close()
            conn.commit()


if __name__ == "__main__":
    read_files_to_db("location_listings.csv")
