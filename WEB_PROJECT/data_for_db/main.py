import os

from flask import Flask, render_template, redirect, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_jwt_extended import JWTManager

from data.db_session import get_session, global_init
from data.users import User
from data.digests import Digests
from data.links import Links
from forms.user import RegisterForm
from forms.adddigest import DigestsForm

from flask_restful import Api

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

if __name__ == '__main__':
    global_init(os.environ.get('DATABASE_URL'))

app = Flask(__name__)
api = Api(app)

import resources

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = 'cliche-argentum-defenestration-dolphin'
jwt = JWTManager(app)


@login_manager.user_loader
def load_user(user_id):
    return get_session().query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Go')


def main():
    global_init(os.environ.get('DATABASE_URL'))

    api.add_resource(resources.UserRegistration, '/api/registration')
    api.add_resource(resources.UserLogin, '/api/login')
    api.add_resource(resources.UserLogoutAccess, '/api/logout/access')
    api.add_resource(resources.UserLogoutRefresh, '/api/logout/refresh')
    api.add_resource(resources.TokenRefresh, '/api/token/refresh')
    api.add_resource(resources.AllUsers, '/api/users')
    api.add_resource(resources.SecretResource, '/api/secret')

    # для локального тестирования
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.route("/")
def index():
    if current_user.is_authenticated:
        digests = get_session().query(Digests).filter(
            (Digests.user == current_user) | (Digests.is_private != True))
    else:
        digests = get_session().query(Digests).filter(Digests.is_private != True)

    return render_template("index.html", digests=digests)


# регистрация новых пользователей
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if get_session().query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        get_session().add(user)
        get_session().commit()
        return redirect('/login')

    return render_template('register.html', title='Register', form=form)


# логин пользоватлей
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_session().query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# редактирование дайджеста
@app.route('/adddigest/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_digest(id):
    form = DigestsForm()
    if request.method == "GET":
        # получаем все дайдесты текущего пользователя
        dg = get_session().query(Digests).filter(Digests.id == id,
                                                 Digests.user == current_user
                                                 ).first()
        if dg:
            form.title.data = dg.title
            form.content.data = dg.content
            form.is_private.data = dg.is_private

            i = 0
            # цикл прохода по всем ссылкам в дайджесте
            for link_elem in form.all_links:
                link_elem.form.link.data = dg.link[0].link
                link_elem.form.description.data = dg.link[0].description
                i += 1

        else:
            # в случае какой-либо ошибки вызываем 404
            abort(404)

    # сохраняем изменения
    if form.validate_on_submit():

        dg = get_session().query(Digests).filter(Digests.id == id,
                                                 Digests.user == current_user
                                                 ).first()
        if dg:
            dg.title = form.title.data
            dg.content = form.content.data
            dg.is_private = form.is_private.data

            i = 0
            for link_elem in form.all_links:
                link = Links(link=link_elem.form.link.data, description=link_elem.form.description.data)
                dg.link[i] = link
                i += 1

            get_session().commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('adddigest.html',
                           title='Edit digest',
                           form=form
                           )


# удаление дайжеста
@app.route('/digest_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    dg = get_session().query(Digests).filter(Digests.id == id,
                                             Digests.user == current_user
                                             ).first()
    if dg:
        for elem in dg.link:
            get_session().delete(elem)
        get_session().delete(dg)
        get_session().commit()
    else:
        abort(404)
    return redirect('/')


# добавление дайджеста
@app.route('/adddigest', methods=['GET', 'POST'])
@login_required
def add_digest():
    form = DigestsForm()
    if form.validate_on_submit():

        print(form.all_links[0].data)

        digest = Digests()
        digest.title = form.title.data
        digest.content = form.content.data
        digest.is_private = form.is_private.data

        print(form.all_links)

        for link_elem in form.all_links:
            link = Links(link=link_elem.form.link.data, description=link_elem.form.description.data)
            digest.link.append(link)

        digest.link.append(link)
        current_user.djs.append(digest)

        get_session().merge(current_user)
        get_session().commit()
        return redirect('/')
    return render_template('adddigest.html', title='Add digest',
                           form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/help')
def help():
    return render_template('help.html')


# страница пользователя
@app.route('/user')
@login_required
def return_user():
    user = get_session().query(User).filter(User.id == current_user.id).first()
    return render_template("user.html", user=user)


if __name__ == '__main__':
    main()
