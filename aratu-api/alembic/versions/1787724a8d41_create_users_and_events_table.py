"""create users and events table

Revision ID: 1787724a8d41
Revises: 
Create Date: 2024-02-07 19:17:19.480763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1787724a8d41'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eventos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.Column('local', sa.String(), nullable=True),
    sa.Column('data_hora', sa.DateTime(), nullable=True),
    sa.Column('valor', sa.Float(), nullable=True),
    sa.Column('foto_url', sa.String(), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eventos_id'), 'eventos', ['id'], unique=False)
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('senha', sa.String(), nullable=True),
    sa.Column('ativo', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_usuarios_id'), table_name='usuarios')
    op.drop_table('usuarios')
    op.drop_index(op.f('ix_eventos_id'), table_name='eventos')
    op.drop_table('eventos')
    # ### end Alembic commands ###
