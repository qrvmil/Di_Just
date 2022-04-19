import datetime
import sqlalchemy
from flask import jsonify
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from . import db_session
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import get_session


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    djs = orm.relation("Digests", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def save_to_db(self):
        db = db_session.create_session()
        db.add(self)
        db.commit()

    def find_by_username(username):
        db = db_session.create_session()
        return db.query(User).filter(User.name == username).first()

    # возвращает всех пользователей
    def return_all():

        news = get_session().query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(only=('name', 'about', 'email', 'created_date'))
                     for item in news]
            }
        )

    # удаляет всех пользователей
    def delete_all():

        try:
            num_rows = get_session().query(User).all()
            for row in num_rows:
                for digest in row.news:
                    for link in digest:
                        get_session().delete(link)
                    get_session().delete(digest)

            num_rows_deleted = get_session().query(User).delete()
            get_session().commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
