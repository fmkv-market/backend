"""initial_schema

Revision ID: 001
Revises:
Create Date: 2026-06-01 16:35:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Таблица user_features с VARCHAR для больших ID
    op.create_table('user_features',
        sa.Column('user_id', sa.String(30), nullable=False),
        sa.Column('user_cart_update_turn_rate', sa.Float(), nullable=False),
        sa.Column('user_click_turn_rate', sa.Float(), nullable=False),
        sa.Column('user_conversion_rate', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('user_id')
    )

    # Таблица item_features
    op.create_table('item_features',
        sa.Column('item_id', sa.String(30), nullable=False),
        sa.Column('item_cart_update_turn_rate', sa.Float(), nullable=False),
        sa.Column('item_click_turn_rate', sa.Float(), nullable=False),
        sa.Column('item_conversion_rate', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('item_id')
    )

    # Таблица user_item_features
    op.create_table('user_item_features',
        sa.Column('user_id', sa.String(30), nullable=False),
        sa.Column('item_id', sa.String(30), nullable=False),
        sa.Column('u2i_cart_updates', sa.Float(), nullable=False),
        sa.Column('u2i_mean_time_between_cartupdates', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'item_id')
    )

    # Таблица item_catalog
    op.create_table('item_catalog',
        sa.Column('item_id', sa.String(30), nullable=False),
        sa.Column('product_category', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('item_id')
    )

    # Таблица item_embeddings
    op.create_table('item_embeddings',
        sa.Column('item_id', sa.String(30), nullable=False),
        sa.Column('embedding', sa.ARRAY(sa.Float()), nullable=False),
        sa.PrimaryKeyConstraint('item_id')
    )


def downgrade():
    op.drop_table('user_features')
    op.drop_table('item_features')
    op.drop_table('user_item_features')
    op.drop_table('item_catalog')
    op.drop_table('item_embeddings')