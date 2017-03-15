from flask import render_template, redirect, url_for, request
from flask_admin.contrib import sqla
from flask_security import Security, SQLAlchemyUserDatastore

from root import app, db, admin, controller

from .auth.user_admin import UserAdmin
from .models import User, Role, Tag
from .forms import SubmitTagForm


data_store = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, datastore=data_store)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = SubmitTagForm(request.form)
    if request.method == 'POST' and form.validate():
        url = form.url.data
        tag = controller.create_tag(url)
        return redirect(url_for('summary', tag=tag))
    return render_template('index.html', title='Main page', form=form)


@app.route('/favicon.ico')
def favicon():
    pass


@app.route('/<string:tag>', methods=['GET'])
def short(tag):
    url = controller.read_url_from_hash(tag)
    if not url:
        url = url_for('error')
    else:
        controller.increment_visit(tag)
    return redirect(url)


@app.route('/error', methods=['GET'])
def error():
    return 'Sorry, wrong tag.'


@app.route('/!<string:tag>', methods=['GET'])
def summary(tag):
    _tag = controller.get_tag_from_hash(tag)
    if _tag:
        return render_template('summary.html', title='Summary', tag=_tag)
    else:
        return redirect(url_for('error'))


admin.add_view(UserAdmin(User, db.session))
admin.add_view(sqla.ModelView(Role, db.session))
admin.add_view(sqla.ModelView(Tag, db.session))
