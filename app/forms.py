from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models import User, City, ProductGroup, Product, Company, Capability, Need, Supply


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    cities = City.query.all()
    a = []
    for city in cities:
        a.append((str(city.id), city.name))
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    phone = StringField('Телефон')
    city = SelectField('Город', choices=a)
    status = SelectField('Статус', choices=[('Потребитель', 'Потребитель'), ('Производитель', 'Производитель')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такой логин уже существует!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот электронный адрес уже зарегистрирован!')


class CitySelectionForm(FlaskForm):
    cities = City.query.all()
    a = [('0', 'Все города')]
    for city in cities:
        a.append((str(city.id), city.name))
    city = SelectField('Город', choices=a)
    submit = SubmitField('Выбрать')
    

class ProductGroupSelectionForm(FlaskForm):
    groups = ProductGroup.query.all()
    a = [('0', 'Все категории')]
    for group in groups:
        a.append((str(group.id), group.name))
    group = SelectField('Категория', choices=a)
    submit = SubmitField('Выбрать')


class CompanyRegistrationForm(FlaskForm):
    name = StringField('Название')
    address = StringField('Адрес')
    submit = SubmitField('Сохранить')


class AddSupplyForm(FlaskForm):
    products = Product.query.all()
    a = []
    for product in products:
        a.append((str(product.id), product.name))
    product = SelectField('Вид продукта', choices=a)
    name = StringField('Название')
    price = IntegerField('Цена')
    submit = SubmitField('Добавить')


class AddProductToUserForm(FlaskForm):
    name = StringField('Название', render_kw={'disabled': 'disabled'})
    price = IntegerField('Цена', render_kw={'disabled': 'disabled'})
    amount = IntegerField('Количество')
    submit = SubmitField('Добавить')


class AddOrderForm(FlaskForm):
    customer_last_name = StringField('Фамилия заказчика')
    customer_first_name = StringField('Имя заказчика')
    customer_phone = StringField('Телефон заказчика')
    company_name = StringField('Производитель', render_kw={'disabled': 'disabled'})
    product_name = StringField('Название продукта', render_kw={'disabled': 'disabled'})
    product_price = IntegerField('Цена продукта', render_kw={'disabled': 'disabled'})
    product_amount = IntegerField('Количество')
    submit = SubmitField('Отправить')


class EditProfileForm(FlaskForm):
    cities = City.query.all()
    a = []
    for city in cities:
        a.append((str(city.id), city.name))
    username = StringField('Логин', validators=[DataRequired()])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    phone = StringField('Телефон')
    city = SelectField('Город', choices=a)
    submit = SubmitField('Сохранить')


class MessageForm(FlaskForm):
    message = TextAreaField('Сообщение', validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Отправить')