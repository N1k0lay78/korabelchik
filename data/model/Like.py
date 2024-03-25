import sqlalchemy
from sqlalchemy.util.preloaded import orm

from data.db_session import SqlAlchemyBase


class Like(SqlAlchemyBase):
    __tablename__ = 'like'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    from_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    to_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    from_user = orm.relationship('User', back_populates="my_like", foreign_keys=[from_user_id])
    to_user = orm.relationship('User', back_populates="like_me", foreign_keys=[to_user_id])
    # decided = sqlalchemy.Column(sqlalchemy.Boolean, server_default="0")
    accepted = sqlalchemy.Column(sqlalchemy.Boolean, server_default="0")
    message = sqlalchemy.Column(sqlalchemy.String)