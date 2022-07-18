import sqlite3
import json

DECODER = json.load(open('sources/db.json'))

class DBManager:

    def connect(self, database_name):
        connector = sqlite3.connect(database_name)
        cursor = connector.cursor()
        return connector, cursor

    def get_db_name(self, decoder):
        return decoder['db_name']

    def get_table_name(self, decoder, index):
        return decoder['tables'][index]

    def create_table(self, cursor, name, *columns):
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} {(','.join(map(str, columns)))}")

    def make_query(self, cursor, query, params):
        if params is None:
            return cursor.execute(query)
        return cursor.execute(query, params)

    def commit_and_close(self, connector):
        connector.commit()
        connector.close()

def main():
    manager = DBManager()
    db_tools = manager.connect(manager.get_db_name(DECODER))
    table = manager.get_table_name(DECODER, 0)
    manager.create_table(db_tools[1], table, 'id', 'value', 'unit', 'result', 'new_unit')
    manager.make_query(db_tools[1], f"INSERT INTO {table} VALUES ({1}, {65}, 'K', {65 - 273.15}, '°C')")
    rows = manager.make_query(db_tools[1], f"SELECT * FROM {table}")
    for row in rows:
        print(row)
    manager.commit_and_close(db_tools[0])

if __name__ == '__main__':
    main()