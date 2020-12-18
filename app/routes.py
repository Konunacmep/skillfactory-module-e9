from flask import render_template, redirect, url_for, jsonify, request, abort, flash
from app import app, db
from app.forms import LoginForm, EventForm
from .models import User, Event
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import functools


# своя страничка для отсутствующего события
def page_not_found(e):
  return render_template('404.html'), 404


# получить словарь всех нужных полей формы, (а не просто всех)
def get_dict_from_form(form):
    return {'time_begin': form.time_begin.data,
            'time_end': form.time_end.data,
            'subject': form.subject.data,
            'description': form.description.data,}

def get_user(username):
    return User.query.filter_by(username=username).first()

# проверим, есть ли следующая страница, или возмем по умолчанию
def go_next(next_page):
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return functools.partial(redirect, next_page)


app.register_error_handler(404, page_not_found)


# регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    # не нужно регистрироваться, если  пользователь уже вошел
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.username.data)
        # Если такой пользователь уже есть, попросим назвать по-другому
        if user is not None:
            flash('Это имя пользователя не доступно')
            return redirect(url_for('register'))
        # создаем пользователя, сохраняем, логиним
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return go_next(request.args.get('next'))()
    # или рисуем пустую форму
    return render_template('login.html', form=form, log=False)


# вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.username.data)
        # проверим, есть ли пользователь, и верен ли его пароль
        if user is None or not user.check_password(form.password.data):
            flash('Не правильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user)
        return go_next(request.args.get('next'))()
    return render_template('login.html', form=form, log=True)

# выход
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# главная
@app.route('/')
@app.route('/index')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)


@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit(event_id):
    event = Event.query.get(event_id)
    # проверим, есть ли такое событие, и принадлежит ли оно текущему пользователю
    if event is None:
        abort(404)
    if event.user_id != current_user.id:
        flash('Вы не можете редактировать чужое событие')
        return redirect(url_for('index'))
    # если да, то рисуем форму и заполняем её
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('event_create_edit.html', form=form, create=False)


# удаление
@app.route('/delete/<int:event_id>', methods=['GET'])
@login_required
def delete(event_id):
    event = Event.query.get(event_id)
    if event is None:
        abort(404)
    if event.user_id != current_user.id:
        flash('Вы не можете удялить чужое событие')
        return redirect(url_for('index'))
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))


# создание
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(**get_dict_from_form(form))
        event.user_id = current_user.id
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('event_create_edit.html', form=form, create=True)
