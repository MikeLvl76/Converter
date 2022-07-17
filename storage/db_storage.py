import sqlite3
import json

def get_db_name(decoder):
    return decoder['db_name']

def get_table_name(decoder, index):
    return decoder['tables'][index]

def create_table(cursor, name, *values):
    cursor.execute(f"DROP TABLE IF EXISTS {name}")
    cursor.execute(f"CREATE TABLE {name} ({','.join(values)})")

def make_query(cursor, query):
    return cursor.execute(query)

def commit_and_close(connector):
    connector.commit()
    connector.close()


def main():
    decoder = json.load(open('sources/db.json'))
    connector = sqlite3.connect(get_db_name(decoder))
    cursor = connector.cursor()
    table = get_table_name(decoder, 0)
    create_table(cursor, table, 'id', 'value', 'unit', 'result', 'new_unit')
    make_query(cursor, f"INSERT INTO {table} VALUES ({1}, {65}, 'K', {65 - 273.15}, '°C')")
    rows = make_query(cursor, f"SELECT * FROM {table}")
    for row in rows:
        print(row)
    commit_and_close(connector)

if __name__ == '__main__':
    main()