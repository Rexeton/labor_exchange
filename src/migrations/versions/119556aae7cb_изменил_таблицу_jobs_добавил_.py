"""Изменил таблицу Jobs,добавил ограничение на зарплату от-до

Revision ID: 119556aae7cb
Revises: e6b667630d8a
Create Date: 2024-07-21 14:48:21.825606

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "119556aae7cb"
down_revision = "e6b667630d8a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "jobs",
        sa.Column("discription", sa.String(), nullable=True, comment="описание вакансии"),
    )
    op.add_column(
        "jobs",
        sa.Column("salary_from", sa.Integer(), nullable=True, comment="Зарплата от"),
    )
    op.add_column(
        "jobs",
        sa.Column("salary_to", sa.Integer(), nullable=True, comment="Зарплата до"),
    )
    op.add_column(
        "jobs",
        sa.Column("is_active", sa.Boolean(), nullable=True, comment="Активна ли вакансия"),
    )
    op.add_column(
        "jobs",
        sa.Column("created_at", sa.DateTime(), nullable=True, comment="Дата создания записи"),
    )
    op.alter_column(
        "users",
        "id",
        existing_type=sa.INTEGER(),
        comment="Идентификатор пользователя",
        existing_comment="Идентификатор задачи",
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "users",
        "is_company",
        existing_type=sa.BOOLEAN(),
        comment="Флаг компании(является ли пользователь компанией)",
        existing_comment="Флаг компании",
        existing_nullable=True,
    )
    op.alter_column(
        "users",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        comment="Дата создания строки",
        existing_comment="Время создания записи",
        existing_nullable=True,
    )
    op.create_unique_constraint(None, "users", ["hashed_password"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.alter_column(
        "users",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        comment="Время создания записи",
        existing_comment="Дата создания строки",
        existing_nullable=True,
    )
    op.alter_column(
        "users",
        "is_company",
        existing_type=sa.BOOLEAN(),
        comment="Флаг компании",
        existing_comment="Флаг компании(является ли пользователь компанией)",
        existing_nullable=True,
    )
    op.alter_column(
        "users",
        "id",
        existing_type=sa.INTEGER(),
        comment="Идентификатор задачи",
        existing_comment="Идентификатор пользователя",
        existing_nullable=False,
        autoincrement=True,
    )
    op.drop_column("jobs", "created_at")
    op.drop_column("jobs", "is_active")
    op.drop_column("jobs", "salary_to")
    op.drop_column("jobs", "salary_from")
    op.drop_column("jobs", "discription")
    # ### end Alembic commands ###
