"""
POC for SQLAlchemy ORM connection to SQLite DB
"""
import os
from sqlalchemy import create_engine, text

db_path = os.path.join(__file__, '..', 'homepage.db')
db_path = os.path.abspath(db_path)
engine = create_engine(f'sqlite+pysqlite:///{db_path}')

def execute(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(str))
    return result

# create a test table and insert a few values
try:
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE test_table (id INT PRIMARY KEY, name VARCHAR(255));"))
        conn.execute(text("INSERT INTO test_table (id, name) VALUES (1,'Alex'), (2, 'Benjamin');"))
        result_1 = conn.execute(
            text("SELECT * FROM User;")
        )
        print(result_1.all())
        result_2 = conn.execute(
            text("SELECT * FROM test_table;")
        )
        print(result_2.all())

    print('debug...')
finally:
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS test_table;"))

