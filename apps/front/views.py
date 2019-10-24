from flask import (
    Blueprint,
    render_template,
    views,

)
bp = Blueprint("home",__name__)

@bp.route('/')
def index():
    return render_template('front/index.html')


class SignUpViews(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

    def post(self):
        pass


bp.add_url_rule('/signup/', view_func=SignUpViews.as_view('signup'))