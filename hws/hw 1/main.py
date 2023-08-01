# ДЗ 1

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')

@app.route('/catalog/')
def catalog():
    return render_template('catalog.html')

@app.route('/bmw/')
def bmw():
    return render_template('bmw.html')

@app.route('/audi/')
def audi():
    return render_template('audi.html')

@app.route('/ford/')
def ford():
    return render_template('ford.html')

@app.route('/hot-rod/')
def hotrod():
    return render_template('hot-rod.html')


if __name__ == '__main__':
    app.run(debug=True)
