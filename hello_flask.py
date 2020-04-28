from flask import Flask
from vsearch import search4letters # importing search4letters

app = Flask(__name__)


@app.route('/') # decorator
def hello() -> str:
    return 'Hello world from Flask!'


@app.route('/search4') # decorator
def do_search() -> str:
    return str(search4letters('life, the universe, and everything', 'eiru,!'))



app.run()
