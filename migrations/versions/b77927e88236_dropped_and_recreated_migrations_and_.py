"""dropped and recreated migrations and tables to overcome error


Revision ID: b77927e88236
Revises: 
Create Date: 2021-11-12 15:40:42.676271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b77927e88236'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('customer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('postal_code', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('register_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('video',
    sa.Column('video_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('total_inventory', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('video_id')
    )
    op.create_table('rental',
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.video_id'], ),
    sa.PrimaryKeyConstraint('video_id', 'customer_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rental')
    op.drop_table('video')
    op.drop_table('customer')
    # ### end Alembic commands ###
