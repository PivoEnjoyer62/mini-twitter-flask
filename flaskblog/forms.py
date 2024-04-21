from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Ім'я користувача",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Емейл',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердити пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Це ім'я користувача вже зайняте. Виберіть будь ласка інше.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Цей емейл вже присутній. Виберіть будь ласка інший.")


class LoginForm(FlaskForm):
    email = StringField('Емейл',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField('Увійти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Нікнейм',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Емейл',
                        validators=[DataRequired(), Email()])
    picture = FileField('Поставити аватар', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Оновити')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Це ім'я вже зайняте. Виберіть інше.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Цей емейл вже присутній. Виберіть будь ласка інший.")


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    content = TextAreaField("Контент", validators=[DataRequired()])
    submit = SubmitField("Пост")

