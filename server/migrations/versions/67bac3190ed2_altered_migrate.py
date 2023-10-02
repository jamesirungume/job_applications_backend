"""altered migrate

Revision ID: 67bac3190ed2
Revises: aae593e4a8eb
Create Date: 2023-10-02 23:53:03.339147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67bac3190ed2'
down_revision = 'aae593e4a8eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('add_job')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('add_job',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=120), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=False),
    sa.Column('location', sa.VARCHAR(length=255), nullable=False),
    sa.Column('company_name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('posted_at', sa.DATETIME(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_add_job_user_id_users'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###