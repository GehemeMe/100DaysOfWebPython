from program import app
from flask import render_template
from datetime import datetime
import requests


@app.route('/')
@app.route('/index')
def index():
    timenow = str(datetime.today())
    return render_template('index.html', time=timenow)

@app.route('/100Days')
def p100Days():
    return render_template('100Days.html')

@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html', joke=joke)

def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']

