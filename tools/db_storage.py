import sqlite3
import json

'''
Class for managing database with sqlite3.
A JSON file is used as storage for database name and tables name.
'''
class DBManager:

    '''
    Initialize class with global variables.
    '''
    def __init__(self) -> None:
        self.decoder = None
        self.connector = None
        self.cursor = None
        self.path = None

    '''
    Fetch data in JSON file by giving its path.
    '''
    def fetch_data(self, filepath):
        self.path = filepath
        self.decoder = json.load(open(filepath, encoding='utf-8'))

    '''
    Connect to database by giving .db filename.
    If the database is new, then its filename is stored in JSON file.
    Be careful to not delete the .db file because it's the database.
    '''
    def connect_to(self, database_name):
        self.connector = sqlite3.connect(database_name)
        if database_name not in self.decoder['databases']:
            self.decoder['databases'].append(database_name)
        self.cursor = self.connector.cursor()

    '''
    Get values from key in JSON file.
    '''
    def get_values(self, key):
        return self.decoder[key]

    '''
    Get item by giving key and index.
    '''
    def get_item(self, key, index):
        if key not in self.decoder.keys():
            return ''
        if len(self.decoder[key]) == 0 or index < 0 or index >= len(self.decoder[key]):
            return ''
        return self.decoder[key][index]

    '''
    Create table using query, by giving name and columns name.
    If the table is new, then its filename is stored in JSON file.
    '''
    def create_table(self, name=str, *columns):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({(','.join(map(str, columns)))})")
        if name not in self.decoder['tables']:
            self.decoder['tables'].append(name)

    '''
    Check if table exists by giving its name.
    '''
    def table_exists(self, table):
        self.make_query(f"SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='{table}');")
        return self.cursor.fetchone()[0]

    '''
    Make a query by giving the query as arg and optionnal parameters.
    '''
    def make_query(self, query, params=None or ()):
        if params is not None:
            return self.cursor.execute(query, params)
        return self.cursor.execute(query)

    '''
    Write new content to JSON.
    '''
    def __write(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.decoder, indent=4))

    '''
    Commit all changes and close connection.
    Then write to JSON what's been added.
    '''
    def commit_and_close(self):
        self.connector.commit()
        self.connector.close()
        self.__write()

    def __str__(self) -> str:
        return json.dumps(self.decoder, indent=4)

def main():
    manager = DBManager()
    manager.fetch_data('sources/db.json')
    manager.connect_to('databases/test.db')
    print(manager.table_exists('zeysgvue'))
    manager.create_table('example', 'id', 'value', 'unit', 'result', 'new_unit')
    table = manager.get_item('tables', 0)
    manager.make_query(f"INSERT INTO {table} VALUES ({1}, {65}, 'K', {65 - 273.15}, '°C')")
    rows = manager.make_query(f"SELECT * FROM {table}")
    for row in rows:
        print(row)
    manager.commit_and_close()
    print(manager)

if __name__ == '__main__':
    main()