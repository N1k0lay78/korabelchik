import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy.sql import func

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    time_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    page = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    is_male = sqlalchemy.Column(sqlalchemy.Boolean)
    # TODO: добавить факультеты в БД
    faculty_id = sqlalchemy.Column(sqlalchemy.Integer)
    is_technical = sqlalchemy.Column(sqlalchemy.Boolean)
    for_people = sqlalchemy.Column(sqlalchemy.String)
    roles = orm.relationship("Role", back_populates="user")
    my_reaction = orm.relationship("Reaction", back_populates="from_user", primaryjoin="User.id==Reaction.from_user_id")
    react_me = orm.relationship("Reaction", back_populates="to_user", primaryjoin="User.id==Reaction.to_user_id")
    warns = sqlalchemy.Column(sqlalchemy.Integer, default=0, server_default="0")
    is_muted_for_people = sqlalchemy.Column(sqlalchemy.Boolean, default=False, server_default="0")
    is_active_questionnaire = sqlalchemy.Column(sqlalchemy.Boolean, default=True, server_default="1")
    # reports_for_people = None
