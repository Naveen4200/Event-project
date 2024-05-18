# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# # Corrected connection string from easy panel
# SQLALCHEMY_DB_URL = "mysql+mysqlconnector://root@localhost/testdb1"
#
# # Create the engine
# engine = create_engine(SQLALCHEMY_DB_URL)
#
# # Create session class
# Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# # Create base class for declarative models
# Base = declarative_base()

# ###########################################################For SSH DB ##############################################

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

# Corrected connection string from easy panel
# SQLALCHEMY_DB_URL = "mysql+mysqlconnector://root:root@localhost:3306/mydatabase"

SQLALCHEMY_DB_URL = 'mysql+pymysql://new_user:new_password@localhost:3306/mydatabase'
# Create the engine
engine = create_engine(SQLALCHEMY_DB_URL)

# Create session class
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()
