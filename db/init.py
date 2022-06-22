import sqlalchemy
import db.tables
import json

psql_url = json.load(open("metadata.json"))["psql_url"]
engine = sqlalchemy.create_engine(psql_url)  # Psql
# engine = sqlalchemy.create_engine('sqlite:///voctab.sqlite3')  # Sqlite


if __name__ == "__main__":
    db.tables.metadata.drop_all(engine)
    db.tables.metadata.create_all(engine)
