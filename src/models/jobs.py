import sqlalchemy as sa
import datetime
from db_settings import Base
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    title = sa.Column(sa.String, comment="Название вакансии")
    discription = sa.Column(sa.String, comment="описание вакансии")
    salary_from = sa.Column(sa.Integer, comment="Зарплата от")
    salary_to = sa.Column(sa.Integer, comment="Зарплата до")
    is_active = sa.Column(sa.Boolean, comment="Активна ли вакансия")
    created_at = sa.Column(sa.DateTime, comment="Дата создания записи", default=datetime.datetime.utcnow)

    users = relationship("User", back_populates="jobs")
    responses = relationship("Response", back_populates="jobs")
    
    #TODO Сделать связь по зарплате, зависимость на создание по FK.is_company (создавать вакансию может только организация) 
    #__table_args__=(
    #    CheckConstraint(salary_to>=salary_from,name="check_salary"),
    #)
