from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import secrets


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    polls = db.relationship('Poll', backref='creator', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator_name = db.Column(db.String(100))
    deadline = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    active = db.Column(db.Boolean, default=True)
    url_hash = db.Column(db.String(16), unique=True, index=True)
    options_to_select = db.Column(db.Integer, default=1)

    options = db.relationship('Option', backref='poll', lazy='dynamic', cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='poll', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super(Poll, self).__init__(*args, **kwargs)
        self.url_hash = secrets.token_hex(8)

    def is_expired(self):
        if not self.deadline:
            return False
        if self.deadline.tzinfo is None:
            deadline_aware = self.deadline.replace(tzinfo=timezone.utc)
        else:
            deadline_aware = self.deadline
        return datetime.now(timezone.utc) > deadline_aware

    def get_results(self):
        # Standard for displaying results
        results = {}
        for option in self.options:
            likes = Vote.query.filter_by(poll_id=self.id, option_id=option.id, vote_type=1).count()
            neutrals = Vote.query.filter_by(poll_id=self.id, option_id=option.id, vote_type=0).count()
            dislikes = Vote.query.filter_by(poll_id=self.id, option_id=option.id, vote_type=-1).count()

            results[option.id] = {
                'option': option,
                'likes': likes,
                'neutrals': neutrals,
                'dislikes': dislikes,
                'score': likes - dislikes
            }

        return results

    def get_optimal_solution(self):
        from solution import find_solution

        voter_sessions = db.session.query(Vote.session_id).filter_by(poll_id=self.id).distinct().all()
        voter_sessions = [vs[0] for vs in voter_sessions]

        preferences = {i: set() for i, _ in enumerate(voter_sessions)}
        allergies = {i: set() for i, _ in enumerate(voter_sessions)}

        for i, session_id in enumerate(voter_sessions):
            liked_votes = Vote.query.filter_by(poll_id=self.id, session_id=session_id, vote_type=1).all()
            for vote in liked_votes:
                option = Option.query.get(vote.option_id)
                preferences[i].add(option.name)  # TODO: Почему не option.id?

            disliked_votes = Vote.query.filter_by(poll_id=self.id, session_id=session_id, vote_type=-1).all()
            for vote in disliked_votes:
                option = Option.query.get(vote.option_id)
                allergies[i].add(option.name)  # TODO: Почему не option.id?

        option_pool = [option.name for option in self.options]  # TODO: Имя или option.id?

        if not voter_sessions:
            return None

        options_to_select = self.options_to_select or 1

        best_solution, metrics, _ = find_solution(
            option_pool,
            options_to_select,
            preferences,
            allergies,
            iterations=100,  # TODO: вынести в конфиг
            steps=1000,
            metrics_coefs=(2, 1)
        )

        # Преобразуем результаты
        optimal_options = []
        for option_name, count in best_solution.items():
            option = Option.query.filter_by(poll_id=self.id, name=option_name).first()
            if option:
                optimal_options.append({
                    'option': option,
                    'count': count
                })

        return {
            'options': optimal_options,
            'metrics': {
                'equality': metrics[0],
                'satisfaction': metrics[1]
            }
        }


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    votes = db.relationship('Vote', backref='option', lazy='dynamic', cascade='all, delete-orphan')


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
    voter_name = db.Column(db.String(100), nullable=False)
    vote_type = db.Column(db.Integer, default=0)  # -1 - dislike, 0 - neutral, 1 - like
    session_id = db.Column(db.String(64), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
