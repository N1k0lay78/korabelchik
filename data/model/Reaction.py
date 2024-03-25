import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy.sql import func

from data.db_session import SqlAlchemyBase


class Reaction(SqlAlchemyBase):
    __tablename__ = 'reaction'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    time_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    # users
    from_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    to_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    from_user = orm.relationship('User', back_populates="my_reaction", foreign_keys=[from_user_id])
    to_user = orm.relationship('User', back_populates="react_me", foreign_keys=[to_user_id])
    # reaction: -2 - warn, -1 - dislike, 0 - no reaction, 1 - like
    reaction = sqlalchemy.Column(sqlalchemy.Integer, default=0, server_default="0")
    is_answered = sqlalchemy.Column(sqlalchemy.Boolean, default=True, server_default="1")
    message = sqlalchemy.Column(sqlalchemy.String, default="", server_default="")

