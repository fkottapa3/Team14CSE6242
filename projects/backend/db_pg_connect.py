import psycopg2
import platform
from sqlalchemy import create_engine

def get_host():
    """
    Determines the appropriate database host based on the runtime environment.
    """
    # Use 'localhost' if running on Windows, otherwise 'host.docker.internal'
    if platform.system() == "Windows":
        return "localhost"
    else:
        return "host.docker.internal"

def connect():
    """
    Connects to the PostgreSQL database using psycopg2.
    """
    try:
        conn = psycopg2.connect(
            dbname='pg_tenant_data',
            user='postgres',
            password='sree420',  # Replace with your actual password
            host=get_host(),
            port='5432'  # Default port for PostgreSQL
        )
        print("Database connection successful.")
        return conn
    except Exception as e:
        print(f"Failed to connect to the database: {e}")

def get_engine():
    """
    Creates and returns an SQLAlchemy engine based on the PostgreSQL connection details.
    """
    # Replace these with your actual credentials
    user='postgres'
    password='sree420'
    host = get_host()
    #host='localhost'
    dbname='pg_tenant_data'
    

    # Construct the connection string
    connection_string = f'postgresql+psycopg2://{user}:{password}@{host}/{dbname}'

    try:
        # Create and return the SQLAlchemy engine
        engine = create_engine(connection_string)
        print("SQLAlchemy engine created successfully.")
        return engine
    except Exception as e:
        print(f"Failed to create SQLAlchemy engine: {e}")


    # Create and return the SQLAlchemy engine
    #engine = create_engine(connection_string)
    #return engine
