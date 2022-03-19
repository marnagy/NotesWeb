from flask import Flask, redirect

app = Flask(__name__)

@app.get('/')
def index():
    return redirect('/test')

@app.get('/test')
def test():
    return { 'Hello': 'world!' }