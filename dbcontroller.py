from PyQt5.QtSql import QSqlDatabase

class DatabaseController:
    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.db = None

    def connect_to_database(self):
        if not self.db:
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.db_path)
            if not self.db.open():
                raise Exception(f"Database Error: {self.db.lastError().text()}")
        return self.db

    def execute_query(self, query):
        # Add method to execute queries and return results
        pass