from datetime import datetime

from flask_security import RoleMixin, UserMixin

from root import db

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime())
    active = db.Column(db.Boolean())
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, **kwargs):
        self.active = True
        self.confirmed_at = datetime.now()
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %s - %s>' % (self.username, self.email)


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    hash = db.Column(db.String(20), unique=True)
    url = db.Column(db.String(), unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship(
        'User',
        foreign_keys='Tag.user_id',
        backref=db.backref('tags', lazy='dynamic')
    )
    visit_count = db.Column(db.Integer())

    def __init__(self, **kwargs):
        self.visit_count = 0
        super(Tag, self).__init__(**kwargs)
