import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USER = os.getenv("COGNODB_USER")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USER, COGNODB_PASSWORD)
)


def test_connection():
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS number")
            record = result.single()

            if record["number"] == 1:
                return True

    except Exception as e:
        print("CognoDB connection error:", e)

    return False


def execute_query(query, parameters=None):
    try:
        with driver.session() as session:
            result = session.run(
                query,
                parameters or {}
            )
            return [record.data() for record in result]

    except Exception as e:
        print("Query error:", e)
        return None