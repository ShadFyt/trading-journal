"""Add ON DELETE CASCADE to annotation.live_trade_id

Revision ID: f7d1998a730b
Revises: 10ba7df0ad2e
Create Date: 2025-08-12 10:58:08.006223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = 'f7d1998a730b'
down_revision: Union[str, None] = '10ba7df0ad2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite can't ALTER constraints. Recreate table with desired FK and copy data.
    op.create_table(
        'annotation_tmp',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('live_trade_id', sa.String(), sa.ForeignKey('live_trade.id', ondelete='CASCADE'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    # Copy existing data
    op.execute(
        sa.text(
            "INSERT INTO annotation_tmp (id, content, date, type, live_trade_id) "
            "SELECT id, content, date, type, live_trade_id FROM annotation"
        )
    )
    # Replace old table
    op.drop_table('annotation')
    op.rename_table('annotation_tmp', 'annotation')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate table without ON DELETE CASCADE and copy data back
    op.create_table(
        'annotation_tmp',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('live_trade_id', sa.String(), sa.ForeignKey('live_trade.id'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.execute(
        sa.text(
            "INSERT INTO annotation_tmp (id, content, date, type, live_trade_id) "
            "SELECT id, content, date, type, live_trade_id FROM annotation"
        )
    )
    op.drop_table('annotation')
    op.rename_table('annotation_tmp', 'annotation')
