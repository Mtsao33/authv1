import databases
import sqlalchemy

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
    "sqlite:///test.db", connect_args={"check_same_thread": False} # enable multithreading

) # allows sqlalchemy to connect to specific type of database

metadata.create_all(engine) # allows engine to use metadata obj to create all col metadata stores
database = databases.Database(
    #config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
    "sqlite:///test.db", force_rollback = True
)  # creates interactable database


