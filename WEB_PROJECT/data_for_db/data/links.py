import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Links(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'links'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    djs_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("digests.id"))
    digest = orm.relation('Digests')

