from typing import Optional
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    abort,
    _app_ctx_stack,
    url_for
)
from flask_cors import CORS
import os
from models import Base, UserModel, engine, SessionLocal, db_session
from sqlalchemy.orm import scoped_session

app = Flask(__name__)
CORS(app)
db_session.__setattr__
app.session = db_session
Base.metadata.create_all(bind=engine)
print('DB created')

logged_in_key = 'logged_in'

# @app.before_first_request
# def before_first():
#     try:
#         db.create_all()
#         Base.metadata.create_all(bind=engine)
#     except: # DB already created
#         pass

@app.get('/')
def index():
    return redirect('/login')

@app.get('/login')
def login():
    if not session.get(logged_in_key):
        return render_template('login.html')
    
    return 'You are logged in, boss 😎'

@app.post('/login')
def log_in():
    username = request.form['username']
    password = request.form['password']

    user: Optional[UserModel] = db_session.query(UserModel).filter(UserModel.username == username).first()

    if not user:
        # wrong username
        flash('Wrong username or password!')
        # return index()
    else:
        user: UserModel
        if not user.checkpwd(password):
            # wrong password
            flash('Wrong username or password!')
            #return index()
        else:
            session[logged_in_key] = True
    return redirect('/login')

@app.get('/register')
def register_template():
    return render_template('register.html')

@app.post('/register')
def register():
    username = request.form['username']
    password = request.form['password']

    user: Optional[UserModel] = db_session.query(UserModel).filter(UserModel.username == username).first()
    if user:
        flash('Username already exists')
        return redirect('/register')
    
    user = UserModel(username, password)
    db_session.add(user)
    db_session.commit()
    return redirect('/login')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run('0.0.0.0', 5000, debug=True)
