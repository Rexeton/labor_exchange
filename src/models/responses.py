import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db_settings import Base


class Response(Base):
    __tablename__ = "responses"

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор отклика",
    )
    user_id = sa.Column(sa.String, comment="Идентификатор пользователя")
    job_id = sa.Column(sa.Integer, sa.ForeignKey("jobs.id"), comment="Идентификатор вакансии")
    message = sa.Column(sa.String, comment="Сопроводительное письмо")
    created_at = sa.Column(
        sa.DateTime, comment="Дата создания записи", default=datetime.datetime.utcnow
    )

    jobs = relationship("Job", back_populates="responses")
