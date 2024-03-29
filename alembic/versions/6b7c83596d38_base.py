"""base

Revision ID: 6b7c83596d38
Revises: 
Create Date: 2024-02-11 16:37:02.914519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b7c83596d38'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), server_default='', nullable=False),
    sa.Column('surname', sa.String(), server_default='', nullable=False),
    sa.Column('verification_code', sa.Integer(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('profile_image', sa.String(), server_default='https://mykaleidoscope.ru/x/uploads/posts/2023-05/1684818829_mykaleidoscope-ru-p-strizhka-stasa-pekhi-pinterest-69.jpg', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('verification_code')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
