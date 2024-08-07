import datetime
from db_settings import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Response(Base):
    __tablename__ = "responses"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор отклика")
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), comment="Идентификатор пользователя")
    job_id = sa.Column(sa.Integer, sa.ForeignKey('jobs.id'), comment="Идентификатор вакансии")
    massage=sa.Column(sa.String,comment="Сопроводительное письмо")
    created_at = sa.Column(sa.DateTime, comment="Дата создания записи", default=datetime.datetime.utcnow)

    users = relationship("User", back_populates="responses")
    jobs = relationship("Job", back_populates="responses")
