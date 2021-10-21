"""empty message

Revision ID: 857ba4585911
Revises: ba388355c74b
Create Date: 2021-10-21 00:47:05.348379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '857ba4585911'
down_revision = 'ba388355c74b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites_people',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('people_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id', 'people_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites_people')
    # ### end Alembic commands ###