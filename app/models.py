from hashlib import md5
from re import A
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from app import db, login


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(UserMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])

@login.user_loader
def load_user(id):
    return User.query.get(str(id))

class CeleryTaskLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(64), index=True, unique=True)
    task_name = db.Column(db.String(64), index=True)
    task_args = db.Column(db.String(64), index=True)
    task_kwargs = db.Column(db.String(64), index=True)
    task_status = db.Column(db.String(64), index=True)
    task_result = db.Column(db.String(64), index=True)
    task_start_time = db.Column(db.String(64), index=True)
    task_end_time = db.Column(db.String(64), index=True)
    task_duration = db.Column(db.String(64), index=True)
    task_traceback = db.Column(db.String(64), index=True)
    task_exception = db.Column(db.String(64), index=True)
    task_user_id = db.Column(db.String(64), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<CeleryTaskLogs {}>'.format(self.task_id)

    def to_dict(self):
        data = {
            'id': self.id,
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_args': self.task_args,
            'task_kwargs': self.task_kwargs,
            'task_status': self.task_status,
            'task_result': self.task_result,
            'task_start_time': self.task_start_time,
            'task_end_time': self.task_end_time,
            'task_duration': self.task_duration,
            'task_traceback': self.task_traceback,
            'task_exception': self.task_exception,
            '_links': {
                'self': url_for('api.get_celery_task_logs', id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['task_id', 'task_name', 'task_args', 'task_kwargs', 'task_status', 'task_result', 'task_start_time', 'task_end_time', 'task_duration', 'task_traceback', 'task_exception']:
            if field in data:
                setattr(self, field, data[field])