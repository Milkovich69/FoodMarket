# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."
bootstrap = Bootstrap(app)

from .models import User, City, Company, ProductGroup, Product, \
    Capability, Need, Supply, MyAdminIndexView, MyModelView, MyUserAdmin

admin = Admin(app, index_view=MyAdminIndexView(menu_icon_type='glyph', menu_icon_value='glyphicon-home'),
              template_mode='bootstrap3')
admin.add_view(MyModelView(City, db.session))
admin.add_view(MyUserAdmin(User, db.session))
admin.add_view(MyModelView(Company, db.session))
admin.add_view(MyModelView(ProductGroup, db.session))
admin.add_view(MyModelView(Product, db.session))
admin.add_view(MyModelView(Capability, db.session))
admin.add_view(MyModelView(Need, db.session))
admin.add_view(MyModelView(Supply, db.session))

if City.query.count() == 0:
    cities = [
        City(name='Агидель'), City(name='Архангельское'), City(name='Баймак'), City(name='Белебей'), City(name='Белорецк'),
        City(name='Бирск'), City(name='Благовещенск'), City(name='Давлеканово'), City(name='Дюртюли'), City(name='Ишимбай'),
        City(name='Красноусольск'), City(name='Кумертау'), City(name='Межгорье'), City(name='Мелеуз'), City(name='Нефтекамск'),
        City(name='Октябрьский'), City(name='Приютово'), City(name='Салават'), City(name='Сибай'), City(name='Старосубхангулово'),
        City(name='Стерлитамак'), City(name='Туймазы'), City(name='Уфа'), City(name='Учалы'), City(name='Чишмы'), City(name='Янаул')
    ]
    for city in cities:
        db.session.add(city)
    db.session.commit()
if ProductGroup.query.count() == 0:
    product_groups = [
        ProductGroup(name='Молочные продукты'),
        ProductGroup(name='Мясо и мясные продукты'),
        ProductGroup(name='Овощи, зелень, ягоды, плоды'),
        ProductGroup(name='Травы и травяные сборы'),
        ProductGroup(name='Мёд'),
        ProductGroup(name='Яйца'),
        ProductGroup(name='Кондитерские изделия'),
        ProductGroup(name='Мучные изделия и хлеб'),
        ProductGroup(name='Безалкогольные напитки'),
        ProductGroup(name='Консервированные продукты')
    ]
    for group in product_groups:
        db.session.add(group)
    db.session.commit()
if Product.query.count() == 0:
    products = [
        Product(name='Молоко коровье', measure='мл.', group_id=1),
        Product(name='Творог', measure='г.', group_id=1),
        Product(name='Сметана', measure='мл.', group_id=1),
        Product(name='Кефир', measure='мл.', group_id=1),
        Product(name='Йогурт', measure='мл.', group_id=1),
        Product(name='Ряженка', measure='мл.', group_id=1),
        Product(name='Фарш говяжий', measure='г.', group_id=2),
        Product(name='Фарш свиной', measure='г.', group_id=2),
        Product(name='Фарш смешанный', measure='г.', group_id=2),
        Product(name='Огурцы', measure='г.', group_id=3),
        Product(name='Помидоры', measure='г.', group_id=3),
        Product(name='Лук репчатый', measure='г.', group_id=3),
        Product(name='Морковь', measure='г.', group_id=3),
        Product(name='Яблоки', measure='г.', group_id=3),
        Product(name='Груши', measure='г.', group_id=3),
        Product(name='Клубника', measure='г.', group_id=3),
        Product(name='Малина', measure='г.', group_id=3),
        Product(name='Мёд липовый', measure='г.', group_id=5),
        Product(name='Мёд цветочный', measure='г.', group_id=5),
        Product(name='Яйца куриные', measure='шт.', group_id=6),
        Product(name='Яйца перепелиные', measure='шт.', group_id=6),
        Product(name='Конфеты шоколадные', measure='г.', group_id=7),
        Product(name='Хлеб пшеничный', measure='шт.', group_id=8),
        Product(name='Хлеб ржаной', measure='шт.', group_id=8),
        Product(name='Батон нарезной', measure='шт.', group_id=8),
        Product(name='Газированная вода Лимонад', measure='мл.', group_id=9),
        Product(name='Минеральная вода газированная', measure='мл.', group_id=9),
        Product(name='Минеральная вода негазированная', measure='мл.', group_id=9),
        Product(name='Говядина тушеная', measure='г.', group_id=10),
        Product(name='Свинина тушеная', measure='г.', group_id=10)
    ]
    for product in products:
        db.session.add(product)
    db.session.commit()

from . import routes, models, errors