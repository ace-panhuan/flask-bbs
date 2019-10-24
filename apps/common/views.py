from flask import Blueprint,render_template

bp = Blueprint("common",__name__,url_prefix="/common")

@bp.route("/")
def index():
    return render_template("common/index.html")


from flask import Blueprint, make_response
from utils.captcha import Captcha
from io import BytesIO

bp = Blueprint('common', __name__, url_prefix='/c')  #common太长，改为c

@bp.route('/')
def index():
    return 'common index'


@bp.route('/graph_captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp