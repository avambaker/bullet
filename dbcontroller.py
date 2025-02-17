from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

class DatabaseController:
    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.db = None

        # Create a single database engine
        engine = create_engine("sqlite:///notes.db")

        # Create a session factory (binds all sessions to the same engine)
        SessionFactory = sessionmaker(bind=engine)

        # Scoped session (thread-safe, recommended for larger apps)
        self.session = scoped_session(SessionFactory)

        # Define base class for models
        self.Base = declarative_base()


    def connect_to_database(self):
        if not self.db:
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.db_path)
            if not self.db.open():
                raise Exception(f"Database Error: {self.db.lastError().text()}")
        return self.db

    def execute_query(self, query, params=None):
        if params is None:
            params = []
        assert isinstance(params, (tuple, list)), "Params must be a tuple or list"
        sql_query = QSqlQuery(self.db)
        if not sql_query.prepare(query):  # ✅ Ensure preparation succeeds
            print(f"Error preparing query: {sql_query.lastError().text()}")
            print("Query:", query)
            return None
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

db_controller = DatabaseController()