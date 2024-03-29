from flask import Flask
import config
from exts import db
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from flask_wtf import CSRFProtect #表单提交防止跨站请求伪造
from exts import mail


def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.config.from_object(config)
    db.init_app(app)
    CSRFProtect(app)
    mail.init_app(app)

    return app





if __name__ == '__main__':
    app = create_app()
    app.run()
