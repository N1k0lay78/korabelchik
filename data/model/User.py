import sqlalchemy
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    page = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # TODO
    roles = None
    age = sqlalchemy.Column(sqlalchemy.Integer)
    is_male = sqlalchemy.Column(sqlalchemy.Boolean)
    # TODO: добавить факультеты в БД
    faculty_id = sqlalchemy.Column(sqlalchemy.Integer)
    is_technical = sqlalchemy.Column(sqlalchemy.Boolean)
    # добавить нужную инфу
