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

    def execute_query(self, query, params):
        sql_query = QSqlQuery(self.db)
        sql_query.prepare(query)
        for val in params:
            sql_query.addBindValue(val)
        if not sql_query.exec_():
            print(f"Error executing query: {sql_query.lastError().text()}")
            print("Attempted query:", query)
            print("Attempted paramters:", params)
            return None
        
        # Collect and return all results
        results = []
        while sql_query.next():
            results.append([sql_query.value(i) for i in range(sql_query.record().count())])
        
        return results