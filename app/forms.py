from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.fields import FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from flask_wtf.file import FileAllowed, FileSize
from app.models import UserModel


# Form:主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 20, message="")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20, message="")])
    password_confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message="Inconsistency between two passwords entered")])
    submit = SubmitField('Register')

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user is not None:
            raise ValidationError('Please use a different email')

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    title = StringField('title', validators=[Length(min=3, max=50), DataRequired()])
    content = TextAreaField('content', validators=[Length(min=3, max=200), DataRequired()])
    post_type = SelectField('Post Type', choices=[
        ('G', 'Gardening'),
        ('HW','HousingWork'),
        ('AC','AfterSchool'),
        ('QA', 'Question'),
        ('Others', 'Others')
    ], validators=[DataRequired()])
    postCode = IntegerField('postcode', validators=[InputRequired(message="missing postcode!"),Length(4,4)])
    submit = SubmitField('POST')


class CommentForm(FlaskForm):
    content = TextAreaField('content', validators=[Length(min=3)])
    post_id = IntegerField('post_id', validators=[InputRequired(message="missing post ID!")])
    submit = SubmitField('POST')


class UploadImageForm(FlaskForm):
    image = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="Invalid image format!"),
                                  FileSize(max_size=1024 * 1024 * 1,
                                           message="The maximum size of the image cannot exceed 1M!")])


class EditAboutMeForm(FlaskForm):
    aboutme = StringField(validators=[Length(min=1, max=50)])


class EditUsernameForm(FlaskForm):
    username = StringField(validators=[Length(min=1, max=10)])

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
