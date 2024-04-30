import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

class Database:
    def __init__(self):
        """
        Initialize the database connection object with the provided database credentials.
        Fetches database credentials from environment variables and constructs the connection URL.
        Raises a ValueError if any of the required credentials are missing.
        """
        # Load environment variables from the .env file
        load_dotenv()

        # Fetch database credentials from environment variables
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_DATABASE")

        # Check if any credentials are missing
        if None in (self.username, self.password, self.host, self.port, self.database):
            raise ValueError("One or more database credentials are missing.")

        self.connection_url = f"postgresql+psycopg2://{self.username}:{self.password}@postgres/{self.database}"
        self.engine = None
        self.connection = None
    
    def connect(self):
        """
        Establishes a connection to the database.

        This function creates a connection engine using the provided connection URL and establishes a connection to the database.
        If the connection is successful, it prints a message indicating that the connection has been established.
        If an exception occurs during the connection process, it prints an error message with the specific exception details.

        Parameters:
            self (DatabaseConnection): The instance of the DatabaseConnection class.

        Returns:
            None
        """
        try:
            self.engine = create_engine(self.connection_url)
            self.connection = self.engine.connect()
            print("Connected to the database.")
        except Exception as e:
            print(f"Error connecting to the database: {str(e)}")

    def execute_query(self, query):
        """
        Executes a SQL query on the database.

        This function executes the provided SQL query on the database using the connection object.
        If the query is successful, it prints a message indicating that the query has been executed.
        If an exception occurs during the query execution, it prints an error message with the specific exception details.

        Parameters:
            self (DatabaseConnection): The instance of the DatabaseConnection class.
            query (str): The SQL query to be executed.

        Returns:
            None
        """
        try:
            df = pd.read_sql_query(query, self.connection)
            return df
        except Exception as e:
            print(f"Error executing query: {str(e)}")

    def close(self):
        """
        Closes the connection to the database.

        This function checks if the connection to the database is open and closes it if it is.
        If the connection is successfully closed, it prints a message indicating that the connection has been disconnected.

        Parameters:
            self (DatabaseConnection): The instance of the DatabaseConnection class.

        Returns:
            None
        """
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def __del__(self):
        self.close()