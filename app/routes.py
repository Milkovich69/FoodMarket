# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from .forms import LoginForm, CitySelectionForm, RegistrationForm, EditProfileForm, \
    CompanyRegistrationForm, ProductGroupSelectionForm, AddSupplyForm, MessageForm
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, City, ProductGroup, Product, Company,\
    Capability, Need, Supply, Message, Notification
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CitySelectionForm()
    users = User.query.filter_by(status='Производитель')
    cities = City.query.all()
    if form.validate_on_submit():
        sel = form.city.data
        if sel != '0':
            users = User.query.filter_by(status='Производитель', city_id=sel).all()
    return render_template('index.html', form=form, users=users, cities=cities)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    last_name=form.last_name.data, first_name=form.first_name.data,
                    phone=form.phone.data, city_id=form.city.data, status=form.status.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    city = City.query.filter_by(id=user.city_id).first_or_404()
    #capabilities = Capability.query.filter_by(user_id=user.id).all()
    #needs = Need.query.filter_by(user_id=user.id).all()
    '''result = dict(request.form)
    if result:
        for key, value in result.items():
            if key == 'capability':
                Capability.query.filter_by(id=value).delete()
            else:
                Need.query.filter_by(id=value).delete()
        db.session.commit()'''
    return render_template('user.html', title='Профиль пользователя', user=user, city=city)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.last_name = form.last_name.data
        current_user.first_name = form.first_name.data
        current_user.phone = form.phone.data
        current_user.city_id = form.city.data
        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.last_name.data = current_user.last_name
        form.first_name.data = current_user.first_name
        form.phone.data = current_user.phone
        form.city.data = str(current_user.city_id)
    return render_template('edit_profile.html', title='Редактирование профиля',
                           form=form)


@app.route('/company_register', methods=['GET', 'POST'])
def company_register():
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data, address=form.address.data, agent_id=current_user.id)
        db.session.add(company)
        db.session.commit()
        flash('Ваша организация зарегистрирована!')
        return redirect(url_for('user', username=current_user.username))
    return render_template('company_register.html', title='Регистрация организации', form=form)


@app.route('/edit_company', methods=['GET', 'POST'])
@login_required
def edit_company():
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        current_user.company.first().name = form.name.data
        current_user.company.first().address = form.address.data
        db.session.commit()
        flash('Изменения сохранены!')
        return redirect(url_for('edit_company'))
    elif request.method == 'GET':
        form.name.data = current_user.company.first().name
        form.address.data = current_user.company.first().address
    return render_template('edit_company.html', title='Редактирование организации', form=form)


@app.route('/products_catalog', methods=['GET', 'POST'])
def products_catalog():
    form = ProductGroupSelectionForm()
    groups = ProductGroup.query.all()
    products = Product.query.all()
    if form.validate_on_submit():
        sel = form.group.data
        if sel != '0':
            products = Product.query.filter_by(group_id=sel).all()
    return render_template('products_catalog.html', title='Каталог продуктов', form=form,
                           products=products, groups=groups)


@app.route('/product/<id>', methods=['GET', 'POST'])
def product(id):
    supplies = Supply.query.filter_by(product_id=id).all()
    product = Product.query.filter_by(id=id).first_or_404()
    companies = Company.query.all()
    groups = ProductGroup.query.all()
    return render_template('product.html', title='Продукт', supplies=supplies, product=product,
                           companies=companies, groups=groups)


@app.route('/add_supply', methods=['GET', 'POST'])
def add_supply():
    form = AddSupplyForm()
    if form.validate_on_submit():
        supply = Supply(company_id=current_user.company.first().id,
                        product_id=form.product.data, price=form.price.data)
        db.session.add(supply)
        db.session.commit()
        flash('Поставка добавлена!')
        return redirect(url_for('user', username=current_user.username))
    return render_template('add_supply.html', title='Добавление поставки', form=form)


@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Сообщение отправлено.')
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title='Отправка сообщения',
                           form=form, recipient=recipient)


@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.now()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', title='Мои сообщения', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
