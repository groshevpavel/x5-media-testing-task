import sqlalchemy as sa

from models.base import metadata

users = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.BigInteger(), primary_key=True),
    sa.Column('firstname', sa.String(length=32)),
    sa.Column('lastname', sa.String(length=64)),
    sa.Column('is_active', sa.Boolean(), default=True),
)
