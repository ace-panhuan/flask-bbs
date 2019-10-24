from flask import(
    Blueprint,
    render_template,
    views,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify
)
from exts import db
import config  # 配置文件
from .froms import LoginForm,RestPwdForm,RestEmailForm  # 表单格式验证器
from .models import CMSUser  # 导入表单，密码加密解密 验证表单
from .decorators import login_required  #导入装饰器
from utils import xjson,xcache
from exts import mail
from flask_mail import Message
import string,random

bp = Blueprint("cms",__name__,url_prefix='/cms')

@bp.route('/test_email/')
def rest_email():
    msg = Message('flask测试邮件',
                  sender='853730490@qq.com',#发送者
                  recipients=['848989599@qq.com'],  #  发送给谁，这里是列表可以给多个人发送
                  body='hello,  这是一封测试邮件，这是邮件正文'
                  )
    mail.send(msg)
    return 'success'



@bp.route('/')
def index():
    print(g.cms_user)
    return render_template('cms/cms_index.html')

@bp.route('/logout/',endpoint='logout')
@login_required
def logout():
    del session[config.CMS_USER_ID]   # 注销登录
    return redirect(url_for('cms.login'))  # 跳转登录

@bp.route('/profile/',endpoint='profile')
@login_required       #判断用户是否登录，登录执行下面函数跳转到cms_profile
def profile():
    return render_template('cms/cms_profile.html')

@bp.route('/email_captcha/')
@login_required
def email_captcha():
    #/cms/emai_capthcha/?email=xxxx@qq.com
    email = request.args.get('email')
    if not email:
        return xjson.json_params_error('请传递邮件参数！')

    #生成6位数的随机验证码
    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x), range(0,10)))
    captcha = ''.join(random.sample(source, 6))

    #发送邮件
    msg = Message('BBS论坛更换邮箱验证码',
                  recipients=[email],
                  body='您的验证码：{},5分钟内有效'.format(captcha))
    try:
        mail.send(msg)
    except Exception as err:
        print(err)
        return xjson.json_server_error(message='邮件发送失败')

    #验证码存入memcached
    xcache.set(email, captcha)
    return xjson.json_success(message='邮件发送成功')



class LoginView(views.MethodView):
    def get(self,message=None):    #是get请求就返回登录页面
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)  # 实例化表单验证器，
        if form.validate():             # 检查用户输入是否按照要求，符合要求返回True!
            email = form.email.data       #获取用户在form表单中提交的email
            password = form.password.data #获取用户在表单中提交的密码
            remember = form.remember.data # 获取用户有没有勾选记住密码，返回1或者0
            user = CMSUser.query.filter_by(email=email).first()  # 从数据库中查询该用户所有信息
            if user and user.check_password(password): # 验证密码，以及user是否为空！
                session[config.CMS_USER_ID] = user.id   # session[config.CMS_USER_ID]这是session的key,给他赋值该用户数据库中的id
                if remember:  # 判断用户是否勾选了 记住我
                    #如果session.permanent = True
                    #session的持久化日期为 31天
                    session.permanent = True    # 给session设置持久化
                return redirect(url_for('cms.index')) # 全部验证成功，返回主页
            else:
                return self.get(message="用户名或者密码错误")
        else:  # 表单验证失败走下一步
            message = form.get_errors()   # 获取错误提示信息
            return self.get(message=message)  # 返回登录页面并提示错误

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))


class ResetPwdView(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        resetpwd_form = RestPwdForm(request.form)
        if resetpwd_form.validate():
            oldpwd = resetpwd_form.oldpwd.data
            newpwd = resetpwd_form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # 因为接受的是ajax,所以这里使用jsonify返回数据
                # 返回code字段表示状态码，message信息提示
                return xjson.json_success("修改成功")
            else:
                return xjson.json_params_error("原密码错误")
        else:
            message = resetpwd_form.get_errors()
            return jsonify({"code": 400, "message": message})


bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))


class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        resetemail_form = RestEmailForm(request.form)
        if resetemail_form.validate():
            email = resetemail_form.email.data
            g.cms_user.email = email
            db.session.commit()
            return xjson.json_success('邮箱修改成功')
        else:
            message = resetemail_form.get_errors()
            return xjson.json_params_error(message)


bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))


