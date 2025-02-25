import logging
import os
import appdirs
import shutil
import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from src.controllers.pathcontroller import resource_path

class DatabaseController:
    def __init__(self):
        self.db = None

        # Set the path to the SQLite database in the app data directory
        self.projects_path = self.get_db_path("projects.db")

        # Create a single database engine
        notes_path = self.get_db_path("notes.db")
        engine = create_engine(f"sqlite:///{notes_path}")

        # Create a session factory (binds all sessions to the same engine)
        SessionFactory = sessionmaker(bind=engine)

        # Scoped session (thread-safe, recommended for larger apps)
        self.session = scoped_session(SessionFactory)

        # Define base class for models
        self.Base = declarative_base()

    def connect_to_database(self):
        if not self.db:
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.projects_path)
            if not self.db.open():
                logging.error(f"File exists: {os.path.exists(self.projects_path)}")
                logging.error(f"Could not open projects.db file at path: {self.projects_path}")
                raise Exception(self.db.lastError().text())
        return self.db

    def execute_query(self, query, params=None):
        if params is None:
            params = []
        assert isinstance(params, (tuple, list)), "Params must be a tuple or list"
        sql_query = QSqlQuery(self.db)
        if not sql_query.prepare(query):  # Ensure preparation succeeds
            logging.error(f"Error preparing query: {sql_query.lastError().text()}")
            logging.info(f"Attempted query: {query}")
            return None
        for val in params:
            sql_query.addBindValue(val)
        if not sql_query.exec_():
            logging.error(f"Error executing query: {sql_query.lastError().text()}")
            logging.info(f"Attempted query: {query}")
            logging.info("Attempted paramters: {params}")
            return None
        
        # Collect and return all results
        results = []
        while sql_query.next():
            results.append([sql_query.value(i) for i in range(sql_query.record().count())])
        return results
    
    def close_connection(self):
        if self.db:
            self.db.close()  # Close the PyQt5 database connection
            self.db = None
        self.session.remove()  # Close the SQLAlchemy session
    
    def get_db_path(self, name):
        # Store the database in a persistent location
        if getattr(sys, 'frozen', False): # if running in a packaged (app) environment
            app_data_dir = appdirs.user_data_dir(appname="bullet", appauthor="AvaBaker")
            os.makedirs(app_data_dir, exist_ok=True)  # Ensure the directory exists
            default_db_path = resource_path("data/" + name)
            logging.debug(f"Default DB Path Exists: {os.path.exists(default_db_path)}")
            persistent_db_path = os.path.join(app_data_dir, name)
            logging.info(f"Running in packaged mode. Default DB path: {default_db_path}, Persistent DB path: {persistent_db_path}")
            self.copy_if_doesnt_exist(default_db_path, persistent_db_path)
            return persistent_db_path
        else: # if running in development mode
            return "data/" + name
    
    def copy_if_doesnt_exist(self, default_db_path, persistent_db_path):
        """Copies the default database to the persistent location if not already present (only in packaged mode)."""
        # Only copy if the database doesn't exist in the persistent location
        if not os.path.exists(persistent_db_path):
            if os.path.exists(default_db_path):
                shutil.copy(default_db_path, persistent_db_path)
                logging.info(f"Copied default database to {persistent_db_path}")
            else:
                logging.warning(f"Default database file {default_db_path} not found!")

db_controller = DatabaseController()