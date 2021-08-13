"""Update the database with variables from files
"""

import psycopg2
import csv

DATABASE_URI = "postgres://kqejfycmueuecf:717cac44aaa9c449627083c73a063dab2f7a7cf7083ee18235537f651af4ad9d@ec2-50-19-176-236.compute-1.amazonaws.com:5432/df64s3e5darhft"


def get_connection():
    """Return connection to database"""
    return psycopg2.connect(DATABASE_URI)


def read_location_listings_to_db(fp):
    """Insert into database locations from `location_listings.csv`

    Args:
        fp (str): Filepath of the csv file.
    """
    with open(fp, "r", newline="") as f:
        rows = csv.reader(f)
        header = next(rows)
        with get_connection() as conn:
            cur = conn.cursor()

            # Reset the indexing of the ID to be from zero.
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
    read_location_listings_to_db("datas/location_listings.csv")
