from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello world!'

@app.route('/info')
def info():
    return 'This is a website written in Flask'

app.run(debug=True)