"""Add unique constraint to Update model.

Revision ID: 369ec4a9d0d4
Revises: 973bc0c61974
Create Date: 2024-11-06 16:58:04.252754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '369ec4a9d0d4'
down_revision = '973bc0c61974'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('software_tool', schema=None) as batch_op:
        batch_op.add_column(sa.Column('update_source', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('update_url', sa.String(length=256), nullable=True))

    with op.batch_alter_table('update', schema=None) as batch_op:
        batch_op.create_unique_constraint('_software_version_uc', ['software_id', 'version'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update', schema=None) as batch_op:
        batch_op.drop_constraint('_software_version_uc', type_='unique')

    with op.batch_alter_table('software_tool', schema=None) as batch_op:
        batch_op.drop_column('update_url')
        batch_op.drop_column('update_source')

    # ### end Alembic commands ###