import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_DATABASE, DB_DRIVER, DB_PASSWORD, DB_SERVER, DB_USERNAME
from app.models.base import Base

connection_string = f"DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD};TrustServerCertificate=yes;"
params = urllib.parse.quote_plus(connection_string)
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
