from flask import *

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.get('/')
def get_index():
    if request.cookies.get('Username'):
        context = {'title': 'Главная',
                   'name': request.cookies.get('Username'),
                   'email': request.cookies.get('Email')}
        return render_template('main.html', **context)
    else:
        return redirect(url_for('login'))


@app.post('/')
def post_index():
    response = redirect(url_for('login'))
    # пробовал разные варианты, а так же ваш код, но работает только так
    for el in request.cookies:
        response.set_cookie(el, expires=0)
    return response


@app.route('/login/', methods=['GET', 'POST'])
def login():
    context = {'title': 'Вход'}
    if request.method == 'POST':
        response = redirect(url_for('get_index'))
        response.headers['new_head'] = 'New value'
        response.set_cookie('Username', request.form.get('name'))
        response.set_cookie('Email', request.form.get('mail'))
        return response
    return render_template('login.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
