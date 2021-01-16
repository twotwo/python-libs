"""init db schema

Revision ID: 2d157466a031
Revises: 
Create Date: 2021-01-08 19:08:05.688762

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "2d157466a031"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """初始化数据结构，适配 sqlite

    [自增主键](https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#using-the-autoincrement-keyword)

    [外键支持](https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support)
    """
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(30), nullable=False, unique=True, comment="登录名"),
        sa.Column("password", sa.VARCHAR(128), nullable=False, comment="密码"),
        sa.Column("role", sa.Integer(), nullable=False, comment="1:超级管理员 2：管理员 3：用户"),
        sa.Column("status", sa.Integer(), nullable=False, comment="0:禁用 1:启用"),
        sa.Column(
            "is_first_login", sa.Integer(), nullable=False, comment="是否首次登录 0:否 1:是"
        ),
        sa.Column("created_at", sa.DATETIME, nullable=False),
        sa.Column("updated_at", sa.DATETIME, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )
    op.create_table(
        "favorite",
        sa.Column(
            "id", sa.Integer(), nullable=False, primary_key=True, autoincrement=True
        ),
        sa.Column(
            "user_fk", sa.Integer(), sa.ForeignKey("user.id"), comment="fk_user_id"
        ),
        sa.Column("patient_id", sa.VARCHAR(255), nullable=False, comment=""),
        sa.Column("study_iuid", sa.VARCHAR(255), nullable=False, comment=""),
        sa.Column("remark", sa.VARCHAR(255), nullable=False, comment=""),
        sa.Column("created_at", sa.DATETIME, nullable=False),
        sa.Column("updated_at", sa.DATETIME, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )
    op.create_table(
        "feedback",
        sa.Column(
            "id", sa.Integer(), nullable=False, primary_key=True, autoincrement=True
        ),
        sa.Column(
            "user_fk", sa.Integer(), sa.ForeignKey("user.id"), comment="fk_user_id"
        ),
        sa.Column("msg", sa.TEXT(), nullable=False, comment=""),
        sa.Column("created_at", sa.DATETIME, nullable=False),
        sa.Column("updated_at", sa.DATETIME, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )
    op.create_table(
        "config",
        sa.Column(
            "id", sa.Integer(), nullable=False, primary_key=True, autoincrement=True
        ),
        sa.Column(
            "user_fk", sa.Integer(), sa.ForeignKey("user.id"), comment="fk_user_id"
        ),
        sa.Column("config", sa.JSON(), nullable=False, comment=""),
        sa.Column("created_at", sa.DATETIME, nullable=False),
        sa.Column("updated_at", sa.DATETIME, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )

    op.execute(
        """INSERT INTO user VALUES (
        1, 'master', 'fbfb386efea67e816f2dda0a8c94a98eb203757aebb3f55f183755a192d44467',
        1, 1, 0, '2020-02-16 19:17:31', '2020-02-16 19:17:38');"""
    )
    op.execute(
        """INSERT INTO user VALUES (
        NULL, 'txadmin', '945b6c53285f3931de0ad822c0e2550a02d1c29d770e57d1eb87a708f3a814f0',
        2, 1, 0, '2020-02-16 19:17:31', '2020-02-16 19:17:38');"""
    )
    op.execute(
        """INSERT INTO user VALUES (
        NULL, 'txdoctor1', 'a6b2df636ed296abfd1d3f9128d2a04ddc3a9621501920518a60493505e96c7d',
        3, 1, 0,  '2020-02-16 19:17:31', '2020-02-16 19:17:38');"""
    )
    op.execute(
        """INSERT INTO user VALUES (
        NULL, 'txdoctor2', 'a6b2df636ed296abfd1d3f9128d2a04ddc3a9621501920518a60493505e96c7d',
        3, 1, 0,  '2020-02-16 19:17:31', '2020-02-16 19:17:38');"""
    )
    op.execute(
        """INSERT INTO user VALUES (
        NULL, 'txdoctor3', 'a6b2df636ed296abfd1d3f9128d2a04ddc3a9621501920518a60493505e96c7d',
        3, 1, 0, '2020-02-16 19:17:31', '2020-02-16 19:17:38');"""
    )
    op.execute(
        """INSERT INTO user VALUES (
        NULL, 'txdoctor4', 'a6b2df636ed296abfd1d3f9128d2a04ddc3a9621501920518a60493505e96c7d',
        3, 1, 0, '2020-02-16 19:17:31', '2020-02-16 19:17:38');"""
    )
    op.execute(
        """INSERT INTO user VALUES (
        NULL, 'txdoctor5', 'a6b2df636ed296abfd1d3f9128d2a04ddc3a9621501920518a60493505e96c7d',
        3, 1, 1, '2020-02-16 19:17:31', '2020-02-16 19:17:38');"""
    )


def downgrade():
    op.drop_table("user")
    op.drop_table("favorite")
    op.drop_table("feedback")
    op.drop_table("config")
