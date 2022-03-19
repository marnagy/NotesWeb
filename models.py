from typing import Any
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine, Date
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from bcrypt import gensalt, hashpw, checkpw
import os
from datetime import date, datetime
from exceptions import InvalidDataException

DB_URI_ENV_KEY = 'DATABASE_URL'

SQLALCHEMY_DB_URI = os.environ[DB_URI_ENV_KEY] if DB_URI_ENV_KEY in os.environ else open('db_uri.txt', 'r').read()
print('DB URI:', SQLALCHEMY_DB_URI)

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
		if not NoteModel.validate(title, body):
			raise InvalidDataException('Note title or note body does not meet required criteria.')

		self.title = title
		self.body = body
		self.parent_id = parent_id
		self.creation = datetime.utcnow()

	@staticmethod
	def validate(title: str, body: str) -> bool:
		return (NoteModel.validate_title(title)
			and NoteModel.validate_body(body))

	@staticmethod
	def validate_title(title: str) -> bool:
		return title is not None and 3 < len(title.strip()) < 50
	
	@staticmethod
	def validate_body(body: str) -> bool:
		return body is not None
	
	def update(self, new_title: str, new_body: str) -> None:
		if not NoteModel.validate(new_title, new_body):
			raise InvalidDataException('New Note Title or New Note Nody does not meet required criteria.')
		
		self.title = new_title
		self.body = new_body

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
