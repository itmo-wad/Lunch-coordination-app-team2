from flask import Blueprint, render_template, session
from flask_login import current_user
from models import Poll

history_routes = Blueprint('history', __name__)


@history_routes.route('/history')
def index():
    if current_user.is_authenticated:
        polls = Poll.query.filter_by(creator_id=current_user.id).order_by(Poll.created_at.desc()).all()
    else:
        if 'created_polls' in session:
            poll_ids = session.get('created_polls', [])
            polls = Poll.query.filter(Poll.id.in_(poll_ids)).order_by(Poll.created_at.desc()).all()
        else:
            polls = []

    return render_template('history.html', polls=polls)