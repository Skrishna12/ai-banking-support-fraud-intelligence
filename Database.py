import mysql.connector as mysql
from sqlalchemy import create_engine

HOST = "localhost"
USER = "root"
PASSWORD = "091267"
DATABASE = "banking_systems"

# MySQL Connector Connection
connection = mysql.connect(
    host= "localhost",
    user= "root",
    password= "091267",
    database= "banking_systems"
)

# SQLAlchemy Engine
DATABASE_URL = (
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
)

engine = create_engine(DATABASE_URL)

print("Connected Successfully")