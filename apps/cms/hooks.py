from .views import bp
import config
from flask import session,g
from .models import CMSUser
from .models import  CMSPersmission

@bp.before_request   # 钩子函数，每次请求之前执行，用法是在请求之前判断用户是否登录
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id) #get查询只能使用ID作为参数，查询一条数据
        if user:              # 如果user有数据，就把他存在 g 里面
            g.cms_user = user




@bp.context_processor
def context_processor():
    return {'CMSPersmission': CMSPersmission}
