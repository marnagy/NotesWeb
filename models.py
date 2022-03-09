from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, checkpw
import uuid

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(150), nullable=False)

    def __init__(self, username: str, email: str, password: str) -> None:
        super().__init__()
        self.username = username
        self.email = email
        salt = uuid.uuid4().hex
        self.pwd_hash = hashpw(password.encode('utf-8'), salt)

    def checkpwd(self, password: str) -> bool:
        return checkpw(password, self.pwd_hash)