from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Corrected connection string from easy panel
SQLALCHEMY_DB_URL = "mysql+mysqlconnector://sql6704492:9gz8hYclY6@sql6.freemysqlhosting.net:3306/sql6704492"

# Create the engine
engine = create_engine(SQLALCHEMY_DB_URL)

# Create session class
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()


def construct_base_url():
    host = "localhost"
    port = 8000
    return f"http://{host}:{port}"
