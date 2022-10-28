"""Adds signal models

Revision ID: 534c316ba65b
Revises: c1abb0cc40e5
Create Date: 2022-10-05 12:28:00.818607

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = "534c316ba65b"
down_revision = "c1abb0cc40e5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "duplication_rule",
        sa.Column("evergreen", sa.Boolean(), nullable=True),
        sa.Column("evergreen_owner", sa.String(), nullable=True),
        sa.Column("evergreen_reminder_interval", sa.Integer(), nullable=True),
        sa.Column("evergreen_last_reminder_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("expression", sa.JSON(), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=True),
        sa.Column("mode", sa.String(), nullable=False),
        sa.Column("search_vector", sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["dispatch_core.dispatch_user.id"],
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "project_id"),
    )
    op.create_index(
        "duplication_rule_search_vector_idx",
        "duplication_rule",
        ["search_vector"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_table(
        "suppression_rule",
        sa.Column("evergreen", sa.Boolean(), nullable=True),
        sa.Column("evergreen_owner", sa.String(), nullable=True),
        sa.Column("evergreen_reminder_interval", sa.Integer(), nullable=True),
        sa.Column("evergreen_last_reminder_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("expression", sa.JSON(), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=True),
        sa.Column("mode", sa.String(), nullable=False),
        sa.Column("expiration", sa.DateTime(), nullable=True),
        sa.Column("search_vector", sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["dispatch_core.dispatch_user.id"],
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "project_id"),
    )
    op.create_index(
        "suppression_rule_search_vector_idx",
        "suppression_rule",
        ["search_vector"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_table(
        "signal",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("external_url", sa.String(), nullable=True),
        sa.Column("external_id", sa.String(), nullable=True),
        sa.Column("severity", sa.String(), nullable=True),
        sa.Column("detection", sa.String(), nullable=True),
        sa.Column("detection_variant", sa.String(), nullable=True),
        sa.Column("raw", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("case_id", sa.Integer(), nullable=True),
        sa.Column("duplication_rule_id", sa.Integer(), nullable=True),
        sa.Column("suppression_rule_id", sa.Integer(), nullable=True),
        sa.Column("search_vector", sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["case.id"],
        ),
        sa.ForeignKeyConstraint(
            ["duplication_rule_id"],
            ["duplication_rule.id"],
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["source.id"],
        ),
        sa.ForeignKeyConstraint(
            ["suppression_rule_id"],
            ["suppression_rule.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "signal_search_vector_idx",
        "signal",
        ["search_vector"],
        unique=False,
        postgresql_using="gin",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("signal_search_vector_idx", table_name="signal", postgresql_using="gin")
    op.drop_table("signal")
    op.drop_index(
        "suppression_rule_search_vector_idx", table_name="suppression_rule", postgresql_using="gin"
    )
    op.drop_table("suppression_rule")
    op.drop_index(
        "duplication_rule_search_vector_idx", table_name="duplication_rule", postgresql_using="gin"
    )
    op.drop_table("duplication_rule")
    # ### end Alembic commands ###