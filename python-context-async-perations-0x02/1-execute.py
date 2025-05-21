import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or []
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = [25]
    with ExecuteQuery("my_database.db", query, params) as results:
        for row in results:
            print(row)
