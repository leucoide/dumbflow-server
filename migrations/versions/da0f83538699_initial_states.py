"""initial states

Revision ID: da0f83538699
Revises: 63dc87c73366
Create Date: 2019-04-20 11:09:27.463120

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Integer, String

# revision identifiers, used by Alembic.
revision = 'da0f83538699'
down_revision = '63dc87c73366'
branch_labels = None
depends_on = None

states_table = sa.sql.table(
    'states',
    sa.sql.column('id', Integer),
    sa.sql.column('name', String),
)


def upgrade():
    state_names = ['Queued', 'Processing', 'Done', 'Errored']
    states = [{'name': name} for name in state_names]

    op.bulk_insert(states_table, states)


def downgrade():
    pass
