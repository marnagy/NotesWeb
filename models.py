from typing import Any
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine, Date
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from bcrypt import gensalt, hashpw, checkpw
import uuid
from datetime import date, datetime

SQLALCHEMY_DB_URI = open('db_uri.txt', 'r').read()

engine = create_engine(
	SQLALCHEMY_DB_URI, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()
#Base.query = db_session.query_property()

class UserModel(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String(80), unique=True, nullable=False)
	email = Column(String(120), unique=True, nullable=False)
	creation = Column(Date, nullable=False)
	pwd_hash = Column(String(150), nullable=False)
	notes = relationship('NoteModel')

	def __init__(self,
		username: str,
		email: str,
		password: str) -> None:
		super().__init__()
		self.username = username
		self.email = email
		self.creation = date.today()
		pwd_encoded = bytes(password, 'utf-8')
		print(f'pwd_encoded: {pwd_encoded}')
		self.pwd_hash = hashpw(pwd_encoded, gensalt())

	def checkpwd(self, password: str) -> bool:
		return checkpw(password.encode('utf-8'), self.pwd_hash)
	
	@staticmethod
	def from_json(json_obj: dict[str, Any]) -> 'UserModel':
		user = UserModel(json_obj['username'], json_obj['email'], '---')
		user.id = json_obj['id']
		user.pwd_hash = json_obj['pwd_hash']
		user.creation = date.fromisoformat(json_obj['creation'])
		user.notes = list(map(NoteModel.from_json, json_obj['notes']))
		return user
	
	def to_json(self) -> dict[str, Any]:
		return {
			'id': self.id,
			'username': self.username,
			'email': self.email,
			'creation': self.creation.isoformat(),
			'pwd_hash': self.pwd_hash,
			'notes': list(
				map(
					lambda note: note.to_json(),
					self.notes
				)
			)
		}

class NoteModel(Base):
	__tablename__ = 'notes'

	id = Column(Integer, primary_key=True)
	parent_id = Column(Integer, ForeignKey('users.id'))
	# parent = relationship("UserModel", backref='users')
	title = Column(String(50), nullable=False)
	body = Column(Text, nullable=False)
	creation = Column(DateTime, nullable=False)

	def __init__(self, title: str, body: str, parent_id: int) -> None:
		super().__init__()
		self.title = title
		self.body = body
		self.parent_id = parent_id
		self.creation = datetime.utcnow()

	def to_json(self) -> dict[str, Any]:
		return {
			'id': self.id,
			'parent_id': self.parent_id,
			'title': self.title,
			'body': self.body,
			'creation': self.creation
		}
	
	@staticmethod
	def from_json(json_obj: dict[str, Any]) -> 'NoteModel':
		note = NoteModel(json_obj['title'], json_obj['body'])
		note.id = json_obj['id']
		note.parent_id = json_obj['parent_id']
		note.creation = json_obj['creation']
		return note
