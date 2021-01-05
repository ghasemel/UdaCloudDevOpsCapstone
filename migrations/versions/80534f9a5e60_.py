"""empty message

Revision ID: 80534f9a5e60
Revises: 
Create Date: 2021-01-05 21:33:53.846665

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '80534f9a5e60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goods',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.VARCHAR(length=400), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('stock', sa.Float(), nullable=False),
    sa.Column('price', postgresql.MONEY(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goods')
    # ### end Alembic commands ###