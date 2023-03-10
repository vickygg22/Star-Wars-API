"""empty message

Revision ID: 5e4831546ff4
Revises: 5d8d42535950
Create Date: 2023-01-24 10:51:32.721037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e4831546ff4'
down_revision = '5d8d42535950'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('password', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_constraint('favorite_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorite_user_id_fkey', 'user', ['user_id'], ['id'])

    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
