import sqlalchemy
from sqlalchemy.util.preloaded import orm

from data.db_session import SqlAlchemyBase


class Role(SqlAlchemyBase):
    __tablename__ = 'role'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship('User', back_populates="roles")
    role_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
