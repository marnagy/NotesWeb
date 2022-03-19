from typing import Optional
from flask import (
	Flask,
	flash,
	redirect,
	render_template,
	request,
	session,
	send_file,
	abort
)
from flask.sessions import SessionMixin
from flask_cors import CORS
import os
from models import Base, NoteModel, UserModel, engine, db_session

app = Flask(__name__,
	template_folder=os.path.join('static', 'html')
)
CORS(app)
app.session = db_session
app.secret_key = 'ac57e30483a72802d4ae83f7b4d889e6b9f3abae7a62b233fb6bd74657510eb6a1cf997a5f127ba976dc2be791f1d598b30c4ab9bd3aa3bcda92ae268d386aaf5ca3004b02ac4bf1255a730652bbc30b62c1cbd518b9c4ade7b48863b85f8c532b36acc3ebf22ffe971ca0eecbdebd7f34ab35f4443d5d92ce2984f37f4d5862'
#Base.metadata.create_all(bind=engine)
print('DB created')

LOGGED_IN_KEY = 'logged_in'
USERMODEL_ID_KEY = 'user'

def logged_in_test(session: SessionMixin) -> bool:
	return LOGGED_IN_KEY in session and session[LOGGED_IN_KEY]

@app.before_first_request
def before_first():
	try:
		Base.metadata.create_all(bind=engine)
	except: # DB already created
		pass

# return static files
@app.get('/static/<dir_name>/<file_name>')
def get_static_file(dir_name: str, file_name: str):
	if ( dir_name in ['html', 'css', 'js'] and
		file_name in os.listdir(os.path.join('static', dir_name))) :
		return send_file(
			os.path.join(
				'static', dir_name, file_name
			)
		)
	return abort(400)

@app.get('/')
def index():
	return redirect('/login')

@app.get('/login')
def login():
	if logged_in_test(session):
		return redirect('/home')

	return render_template('login.html')

@app.post('/login')
def log_in():
	username = request.form['username']
	password = request.form['password']

	user: Optional[UserModel] = db_session.query(UserModel).filter(UserModel.username == username).first()

	if not user:
		# wrong username
		flash('Wrong username or password!', 'info')
	else:
		user: UserModel
		if not user.checkpwd(password):
			# wrong password
			flash('Wrong username or password!')
		else:
			session[LOGGED_IN_KEY] = True
			session[USERMODEL_ID_KEY] = user.id
			flash('You are signed in!')
	return redirect('/login')

@app.get('/register')
def register_template():
	return render_template('register.html')

@app.post('/register')
def register():
	username = request.form['username']
	email = request.form['email']
	password = request.form['password']

	user: Optional[UserModel] = db_session.query(UserModel).filter(UserModel.username == username).first()
	if user:
		flash('Username already exists')
		return redirect('/register')
	
	user = UserModel(username, email, password)
	db_session.add(user)
	db_session.commit()
	return redirect('/login')

##### logged in only #####
@app.get('/home')
def home():
	if not logged_in_test(session):
		return redirect('/login')

	current_user_id = session[USERMODEL_ID_KEY]
	current_user = db_session.query(UserModel).filter(UserModel.id == current_user_id).first()
	return render_template('home.html', user=current_user, user_creation=current_user.creation.strftime('%d.%m.%Y'))

@app.get('/add_note')
def add_note_template():
	if not logged_in_test(session):
		return redirect('/login')
	
	return render_template('new_note.html')

@app.post('/add_note')
def add_note():
	title = request.form['title']
	body = request.form['body']

	if not (3 <= len(title) <= 50 and body is not None):
		abort(400)
	
	note = NoteModel(title, body, int(session[USERMODEL_ID_KEY]))
	db_session.add(note)
	db_session.commit()
	return redirect('/home')

@app.get('/note/<int:note_id>')
def shot_note(note_id: int):
	if not logged_in_test(session):
		return redirect('/login')
	
	current_user_id = session[USERMODEL_ID_KEY]
	note = db_session.query(NoteModel).filter(NoteModel.id == note_id, NoteModel.parent_id == current_user_id).first()

	if note is None:
		abort(400)
	
	print(f'Note body:\n"{note.body}"')
	return render_template('show_note.html', note=note)

@app.post('/note/<int:note_id>')
def update_note(note_id: int):
	if not logged_in_test(session):
		return redirect('/login')

	new_title = request.form['title']
	new_body = request.form['body']

	current_user_id = session[USERMODEL_ID_KEY]
	note = db_session.query(NoteModel).filter(NoteModel.id == note_id, NoteModel.parent_id == current_user_id).first()

	if note is None:
		abort(400)
	
	note.update(new_title, new_body)
	db_session.commit()
	return redirect(f'/note/{note_id}')

@app.get('/note/delete/<int:note_id>')
def delete_note(note_id: int):
	if not logged_in_test(session):
		return redirect('/login')

	current_user_id = session[USERMODEL_ID_KEY]
	note = db_session.query(NoteModel).filter(NoteModel.id == note_id, NoteModel.parent_id == current_user_id).first()

	if note is None:
		abort(400)
	
	db_session.delete(note)
	db_session.commit()
	return redirect('/home')

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run('0.0.0.0', 5000, debug=True)
