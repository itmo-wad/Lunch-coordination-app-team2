from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import current_user, login_required
from models import Poll

history_routes = Blueprint('history', __name__)


@history_routes.route('/history')
@login_required
def index():
    polls = Poll.query.filter_by(creator_id=current_user.id).order_by(Poll.created_at.desc()).all()
    return render_template('history.html', polls=polls)
