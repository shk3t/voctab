from sqlalchemy import Column, String, Integer, PrimaryKeyConstraint
import sqlalchemy

metadata = sqlalchemy.MetaData()


entries = sqlalchemy.Table(
    "entries",
    metadata,
    Column("en_content", String(64)),
    Column("ru_content", String(64)),
    Column("success_count", Integer(), default=0),
    Column("fail_count", Integer(), default=0),
    PrimaryKeyConstraint("en_content", "ru_content"),
    schema="voctab",
)
