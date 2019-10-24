from ..forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import InputRequired,Email,Length,EqualTo,ValidationError
#{'password': ['密码长度在6-20位'], 'password_repeat': ['密码长度在6-20位', '两次密码必须一致']}
from utils import xcache
from .models import CMSUser


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱类型"),InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(6,20,message="请输入正确格式的密码")])
    remember = IntegerField()


class RestPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message="请输入6位以上的密码")])
    newpwd = StringField(validators=[Length(6,20,message="请输入6位以上的密码")])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message="新密码输入不一致")])



class RestEmailForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式错误'),InputRequired(message='请输入邮箱') ])
    captcha = StringField(validators=[Length(min=6, max=6, message='验证码长度错误')])

    def validate_email(self, field):
        user = CMSUser.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('该邮箱已存在')

    def validate_captcha(self, field):
        email = self.email.data
        captcha = field.data
        captcha_cache = xcache.get(email)
        #判断memcached中是否有对应的邮箱及验证码，小写进行比较，这样用户可以不区分大小写
        if  not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')

