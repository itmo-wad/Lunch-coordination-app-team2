from flask import Blueprint, render_template, redirect, url_for, flash, request, session, abort
from flask_login import current_user
from models import Poll, Option, Vote
from forms import PollForm, OptionForm, VoteForm
from app import db
import uuid

poll_routes = Blueprint('polls', __name__)


@poll_routes.route('/')
def index():
    active_polls = Poll.query.filter_by(active=True).order_by(Poll.created_at.desc()).all()
    return render_template('index.html', polls=active_polls)


@poll_routes.route('/new', methods=['GET', 'POST'])
def create_poll():
    form = PollForm()
    if form.validate_on_submit():
        poll = Poll(
            title=form.title.data,
            description=form.description.data,
            deadline=form.deadline.data
        )

        if current_user.is_authenticated:
            poll.creator_id = current_user.id
        else:
            poll.creator_name = form.creator_name.data

        db.session.add(poll)
        db.session.commit()  # Commit here to get poll.id

        # Now that we have poll.id, add it to the session
        if not current_user.is_authenticated:
            if 'created_polls' not in session:
                session['created_polls'] = []
            session['created_polls'].append(poll.id)
            session.modified = True

        flash('Poll created successfully!')
        return redirect(url_for('polls.add_options', poll_id=poll.id))

    return render_template('polls/create.html', form=form)


@poll_routes.route('/polls/<int:poll_id>/options', methods=['GET', 'POST'])
def add_options(poll_id):
    poll = Poll.query.get_or_404(poll_id)

    # Modified authorization check
    is_authorized = False
    if current_user.is_authenticated and poll.creator_id == current_user.id:
        is_authorized = True
    elif not current_user.is_authenticated and 'created_polls' in session and poll_id in session['created_polls']:
        is_authorized = True

    if not is_authorized:
        flash('You do not have permission to add options to this poll.')
        return redirect(url_for('polls.index'))

    form = OptionForm()

    if form.validate_on_submit():
        option = Option(
            poll_id=poll_id,
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(option)
        db.session.commit()

        flash('Option added!')
        return redirect(url_for('polls.add_options', poll_id=poll_id))

    options = Option.query.filter_by(poll_id=poll_id).all()
    return render_template('polls/options.html', poll=poll, form=form, options=options)


@poll_routes.route('/p/<string:poll_hash>', methods=['GET', 'POST'])
def view(poll_hash):
    poll = Poll.query.filter_by(url_hash=poll_hash).first_or_404()

    # Check if the poll has options
    options = Option.query.filter_by(poll_id=poll.id).all()
    if not options:
        flash('This poll has no options to vote on yet.')
        return redirect(url_for('polls.index'))

    if not poll.active or poll.is_expired():
        return redirect(url_for('polls.results', poll_hash=poll_hash))

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    existing_vote = Vote.query.filter_by(
        poll_id=poll.id,
        session_id=session['session_id']
    ).first()

    if existing_vote:
        flash('You have already voted in this poll.')
        return redirect(url_for('polls.results', poll_hash=poll_hash))

    form = VoteForm()

    if form.validate_on_submit():
        for option in options:
            vote_type = request.form.get(f'vote_{option.id}', 0)

            vote = Vote(
                poll_id=poll.id,
                option_id=option.id,
                vote_type=int(vote_type),
                voter_name=form.voter_name.data,
                session_id=session['session_id']
            )
            db.session.add(vote)

        db.session.commit()
        flash('Your vote has been recorded!')
        return redirect(url_for('polls.results', poll_hash=poll_hash))

    return render_template('polls/view.html', poll=poll, form=form, options=options)


@poll_routes.route('/p/<string:poll_hash>/results')
def results(poll_hash):
    poll = Poll.query.filter_by(url_hash=poll_hash).first_or_404()
    results = poll.get_results()

    sorted_results = sorted(
        results.values(),
        key=lambda x: x['score'],
        reverse=True
    )

    return render_template('polls/results.html', poll=poll, results=sorted_results)


@poll_routes.route('/p/<string:poll_hash>/finish', methods=['POST'])
def finish_poll(poll_hash):
    poll = Poll.query.filter_by(url_hash=poll_hash).first_or_404()

    # Check permissions to finish the poll
    if current_user.is_authenticated and poll.creator_id == current_user.id:
        authorized = True
    elif not current_user.is_authenticated and 'created_polls' in session and poll.id in session['created_polls']:
        authorized = True
    else:
        authorized = False

    if not authorized:
        abort(403)

    poll.active = False
    db.session.commit()

    flash('Poll successfully completed.')
    return redirect(url_for('polls.results', poll_hash=poll_hash))