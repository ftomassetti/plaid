from flask import Response, Blueprint, session
from flask import g, render_template, url_for
from flask import request, abort, redirect
from flask.ext.security import current_user
from app.forms import ProfileForm
from flask import request, flash

from flask.ext.security.utils import encrypt_password

from app import app
from app import db

bp = Blueprint('user', __name__, url_prefix='/profile')

@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = ProfileForm(request.form, current_user)
    if request.method == 'POST' and form.validate():
        form.populate_obj(current_user)
        current_user.password = encrypt_password(current_user.password)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('profile.html', form=form, profile=current_user)
