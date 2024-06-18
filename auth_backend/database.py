import databases
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DEV_DATABASE_URL')

#from config import config

metadata = sqlalchemy.MetaData() # stores data about our db

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    #config.DATABASE_URL, connect_args={"check_same_thread": False} # enable multithreading
    DATABASE_URL#, connect_args={"check_same_thread": False} # enable multithreading, only for sqlite

) # allows sqlalchemy to connect to specific type of database

metadata.create_all(engine) # allows engine to use metadata obj to create all col metadata stores
database = databases.Database(
    #config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
    DATABASE_URL, force_rollback = True
)  # creates interactable database


