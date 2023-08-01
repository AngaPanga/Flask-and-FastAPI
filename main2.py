from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    response = make_response("Cookie установлен")
    response.set_cookie('username', 'admin')
    return response


@app.route('/getcookie/')
def get_cookies():
    name = request.cookies.get('username')
    return f"Значение cookie: {name}"


if __name__ == '__main__':
    app.run(debug=True)