from PyQt5.QtSql import QSqlDatabase, QSqlQuery

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
        sql_query = QSqlQuery(self.db)
        if not sql_query.exec(query):
            print(f"Error executing query: {sql_query.lastError().text()}")
            return None
        
        # Collect and return all results
        results = []
        while sql_query.next():
            results.append([sql_query.value(i) for i in range(sql_query.record().count())])
        
        return results