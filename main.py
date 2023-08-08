from flask import *
from flask_wtf import CSRFProtect
from models import *
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_base.db'
db.init_app(app)

app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'
csrf = CSRFProtect(app)


@app.route('/')
def hi():
    return "OK"


@app.route('/lock/', methods=['GET', 'POST'])
def lock():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        login = form.login.data
        password = form.password.data
        exis_user = User.query.filter_by(login=login).first()
        if exis_user and check_password_hash(exis_user.password, password):
            return 'Lock in is successful'
        else:
            form.login.errors.append('Пользователя с таким логином не существует!')
            form.password.errors.append('Или пароль неверный!')
            return render_template('lock.html', form=form)
    return render_template('lock.html', form=form)


@app.route('/reg/', methods=['GET', 'POST'])
def reg_form():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Взятие данных из формы
        login = form.login.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        # Поиск пользователя в БД
        exis_user = User.query.filter(User.login == login).first()
        if exis_user:
            form.login.errors.append('Пользователь с таким логином уже существует!')
            return render_template('registration.html', form=form)
        user = User(login=login, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return 'Registration success!'
    return render_template('registration.html', form=form)


# Помню что передавать чистые данные нельзя, но смог разобраться с плагином на чтение бд
@app.route('/dbu/')
def db_users():
    users = User.query.all()
    context = {'users': users}
    return render_template('db.html', **context)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print('OK')
    app.run(debug=True)

