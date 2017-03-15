import hashlib

from flask_security import utils
from sqlalchemy import func
import os
from random import randint


class Controller(object):
    @staticmethod
    def create_user(user_data):
        from app.app import db, data_store
        data_store.create_user(
            username=user_data.get('login').get('username'),
            first_name=user_data.get('name').get('first'),
            last_name=user_data.get('name').get('last'),
            email=user_data.get('email'),
            password=utils.encrypt_password(user_data.get('login').get('password')),
        )
        db.session.commit()

    @staticmethod
    def get_tag_from_hash(_hash):
        from app.models import Tag
        tag = Tag.query.filter_by(hash=_hash).first()
        return tag

    def read_url_from_hash(self, _hash):
        tag = self.get_tag_from_hash(_hash)
        return tag.url if tag else None

    @staticmethod
    def read_hash_from_url(url):
        from app.models import Tag
        tag = Tag.query.filter_by(url=url).first()
        return tag.hash if tag else None

    def pick_hash(self, url):
        from app.models import Tag
        from app.app import app
        left, right = app.config.get('SHORT_URL_LENGTH_BOUNDS')
        _hash = hashlib.sha256(('%s%s' % (
            url, os.urandom(8)
        )).encode('utf-8')).hexdigest()[:randint(left, right)]
        if Tag.query.filter_by(hash=_hash).first():
            return self.pick_hash(url)
        else:
            return _hash

    @staticmethod
    def pick_user():
        from app.models import User
        return User.query.order_by(func.random()).first()

    def create_tag(self, url):
        from app.models import Tag
        from app.app import db
        http = 'http://'
        https = 'https://'
        if http not in url or https not in url:
            url = '%s%s' % (http, url)
        _hash = self.read_hash_from_url(url)
        if _hash:
            return _hash
        else:
            tag = Tag(
                url=url,
                hash=self.pick_hash(url),
                user=self.pick_user()
            )
            db.session.add(tag)
            db.session.commit()
            return tag.hash

    def increment_visit(self, _hash):
        from app.app import db
        tag = self.get_tag_from_hash(_hash)
        tag.visit_count += 1
        db.session.commit()
