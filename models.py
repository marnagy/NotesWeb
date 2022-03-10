from sqlalchemy import Column, Integer, String, create_engine
import sqlalchemy
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from bcrypt import gensalt, hashpw, checkpw
import uuid

SQLALCHEMY_DB_URI = 'sqlite:///test.db'

engine = create_engine(
    SQLALCHEMY_DB_URI, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()
Base.query = db_session.query_property()

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    pwd_hash = Column(String(150), nullable=False)

    def __init__(self,
        username: str, #email: str,
        password: str) -> None:
        super().__init__()
        self.username = username
        #self.email = email
        pwd_encoded = bytes(password, 'utf-8')
        print(f'pwd_encoded: {pwd_encoded}')
        self.pwd_hash = hashpw(pwd_encoded, gensalt())

    def checkpwd(self, password: str) -> bool:
        return checkpw(password.encode('utf-8'), self.pwd_hash)