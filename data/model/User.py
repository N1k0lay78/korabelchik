import sqlalchemy
from sqlalchemy.util.preloaded import orm

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    page = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    is_male = sqlalchemy.Column(sqlalchemy.Boolean)
    # TODO: добавить факультеты в БД
    faculty_id = sqlalchemy.Column(sqlalchemy.Integer)
    is_technical = sqlalchemy.Column(sqlalchemy.Boolean)
    # добавить нужную инфу
    for_people = sqlalchemy.Column(sqlalchemy.String)
    # for_interests = sqlalchemy.Column(sqlalchemy.String)
    # TODO
    is_muted_for_people = sqlalchemy.Column(sqlalchemy.Boolean, default=False, server_default="0")
    # is_muted_for_interests = sqlalchemy.Column(sqlalchemy.Boolean, default=False, server_default="0")
    reports_for_people = None
    # reports_for_interests = None
    # END
    roles = orm.relationship("Role", back_populates="user")
