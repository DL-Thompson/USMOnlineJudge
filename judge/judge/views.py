from judge import app
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)
	
@app.route('/')
def front_page():
	return 'USM Online Judge main page'