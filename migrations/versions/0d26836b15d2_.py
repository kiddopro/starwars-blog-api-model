"""empty message

Revision ID: 0d26836b15d2
Revises: 14e21f995b34
Create Date: 2021-10-21 04:31:01.506019

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0d26836b15d2'
down_revision = '14e21f995b34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('people', 'name',
               existing_type=mysql.VARCHAR(length=150),
               nullable=False)
    op.alter_column('planets', 'name',
               existing_type=mysql.VARCHAR(length=150),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('planets', 'name',
               existing_type=mysql.VARCHAR(length=150),
               nullable=True)
    op.alter_column('people', 'name',
               existing_type=mysql.VARCHAR(length=150),
               nullable=True)
    # ### end Alembic commands ###
