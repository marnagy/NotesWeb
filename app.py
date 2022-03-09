from typing import Optional
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    abort
)
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////temp/test.db'
from models import db, UserModel
db.init_app(app)

# ! crashes here
db.create_all(app) 

logged_in_key = 'logged_in'

# @app.before_first_request
# def before_first():
#     try:
    # except: # DB already created
    #     pass

@app.get('/')
def index():
    if not session.get(logged_in_key):
        return render_template('login.html')
    
    return 'You are logged in, boss 😎'

@app.post('/login')
def log_in():
    username = request.form['username']
    password = request.form['password']

    user: Optional[UserModel] = UserModel.filter_by(username=username).first()

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
    return index()

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run('0.0.0.0', 5000, debug=True)
