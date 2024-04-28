from datetime import datetime

from sqlalchemy import Integer, String, Column, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column("id", Integer, primary_key=True)
    login = Column("email", String, nullable=False)
    username = Column('username', String, unique=True)
    password = Column("password", String, nullable=False)
    created_at = Column("registered_at", TIMESTAMP, default=datetime.utcnow)
    project_id = Column("project_id", Integer, primary_key=True)
