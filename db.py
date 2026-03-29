import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        column_defs = ', '.join([f'{col_name} {data_type}' for col_name, data_type in columns.items()])
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})')
        self.connection.commit()

    def insert(self, table_name, values):
        placeholders = ', '.join(['?'] * len(values))
        self.cursor.execute(f'INSERT INTO {table_name} VALUES ({placeholders})', values)
        self.connection.commit()

    def query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()