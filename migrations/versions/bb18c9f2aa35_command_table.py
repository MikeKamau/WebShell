"""Command table

Revision ID: bb18c9f2aa35
Revises: fc8845d0f53f
Create Date: 2019-02-05 14:02:43.068065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb18c9f2aa35'
down_revision = 'fc8845d0f53f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('command',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('command', sa.String(length=128), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_command_timestamp'), 'command', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_command_timestamp'), table_name='command')
    op.drop_table('command')
    # ### end Alembic commands ###