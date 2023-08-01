from flask import *

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.get('/')
def get_index():
    #if request.cookies.get('Username'):
    return f"Привет, {request.cookies.get('Username')}" \
            f"<br>e-mail  -  {request.cookies.get('Email')}"
    #else:
    #    return redirect(url_for('login'))


@app.post('/')
def post_index():
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    context = {'title': 'Вход'}
    response = make_response(render_template('login.html', **context))
    if request.method == 'POST':
        response.set_cookie('Username', request.form.get('name'))
        response.set_cookie('Email', request.form.get('mail'))
        return redirect(url_for('index'))
    return response


if __name__ == '__main__':
    app.run(debug=True)
