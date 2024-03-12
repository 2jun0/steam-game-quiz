"""0006-GAME-ALIAS-GAME-ID-NAME-UNIQUE

Revision ID: cc7150130bcf
Revises: d8e0e8e12a4a
Create Date: 2024-03-12 01:40:10.343486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'cc7150130bcf'
down_revision: Union[str, None] = 'd8e0e8e12a4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='game_alias')
    op.create_unique_constraint(None, 'game_alias', ['game_id', 'name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'game_alias', type_='unique')
    op.create_index('name', 'game_alias', ['name'], unique=True)
    # ### end Alembic commands ###
