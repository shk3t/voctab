import sqlalchemy.dialects.postgresql as psqldb
from sqlalchemy.sql.expression import func
from sqlalchemy import bindparam, and_
import sqlalchemy

import db.init
from db.tables import entries
from utils import df_to_sqlable


def execute(stmt, df=None):
    with db.init.engine.connect() as conn:
        if df is not None:
            return conn.execute(stmt, df_to_sqlable(df))
        return conn.execute(stmt)


def select_random_entries():
    stmt = sqlalchemy.select(entries).order_by(func.random())
    return execute(stmt)

def select_unsuc_random_entries():
    stmt = sqlalchemy.select(entries).order_by(func.random()).where(
        entries.c.success_count - entries.c.fail_count < 3
    )
    return execute(stmt)

def insert_entries(df):
    stmt = psqldb.insert(entries).on_conflict_do_nothing()  # Psql
    # operation = db.insert(entries).prefix_with("OR IGNORE")  # Sqlite
    return execute(stmt, df)


def update_stats(df):
    df = df.rename(columns={"en_content": "b_en_content", "ru_content": "b_ru_content"})
    stmt = (
        sqlalchemy.update(entries)
        .where(
            and_(
                entries.c.en_content == bindparam("b_en_content"),
                entries.c.ru_content == bindparam("b_ru_content"),
            )
        )
        # .values(
        #     success_count=bindparam("success_count"),
        #     fail_count=bindparam("fail_count"),
        # )
    )
    return execute(stmt, df)
