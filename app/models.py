from app import db, login
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for,flash
from datetime import datetime
import json
from time import time
from flask_admin import AdminIndexView


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    users = db.relationship('User', backref='from_city', lazy='dynamic')

    def __repr__(self):
        return '<Населенный пункт {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(32))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    status = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    capabilities = db.relationship('Capability', backref='owner', lazy='dynamic')
    needs = db.relationship('Need', backref='owner', lazy='dynamic')
    company = db.relationship('Company', backref='agent', lazy='dynamic')
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):
        return '<Пользователь {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=mp&s={}'.format(digest, size)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    address = db.Column(db.String(100))
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    supplies = db.relationship('Supply', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Компания {}>'.format(self.name)


class ProductGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    products = db.relationship('Product', backref='by_group', lazy='dynamic')

    def __repr__(self):
        return '<Группа продуктов {}>'.format(self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    measure = db.Column(db.String(16))
    group_id = db.Column(db.Integer, db.ForeignKey('product_group.id'))
    supplies = db.relationship('Supply', backref='product', lazy='dynamic')

    def __repr__(self):
        return '<Продукт {}>'.format(self.name)


class Capability(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('supply.id'), primary_key=True)
    amount = db.Column(db.Integer)


class Need(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('supply.id'), primary_key=True)
    amount = db.Column(db.Integer)


class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    name = db.Column(db.String(100), index=True)
    price = db.Column(db.Integer)
    capabilities = db.relationship('Capability', backref='cap_product', lazy='dynamic')
    needs = db.relationship('Need', backref='need_product', lazy='dynamic')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    customer_last_name = db.Column(db.String(32))
    customer_first_name = db.Column(db.String(32))
    customer_phone = db.Column(db.String(32))
    company_id = db.Column(db.Integer)
    company_name = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    product_price = db.Column(db.Integer)
    product_amount = db.Column(db.Integer)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return '<Сообщение {}>'.format(self.body)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


class MyModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_anonymous:
            return current_user.id == 1

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_anonymous:
            if current_user.id != 1:
                flash('У вас нет доступа к этой странице, так как Вы не администратор!')
        return redirect(url_for('login'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_anonymous:
            return current_user.id == 1

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_anonymous:
            if current_user.id != 1:
                flash('У вас нет доступа к этой странице, так как Вы не администратор!')
        return redirect(url_for('login'))


class MyUserAdmin(ModelView):
    column_exclude_list = ('password_hash',)

    def is_accessible(self):
        if not current_user.is_anonymous:
            return current_user.id == 1

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_anonymous:
            if current_user.id != 1:
                flash('У вас нет доступа к этой странице, так как Вы не администратор!')
        return redirect(url_for('login'))