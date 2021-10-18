import sqlalchemy as sa

from models.base import metadata

bonuses = sa.Table(
    'bonuses',
    metadata,
    sa.Column('id', sa.BigInteger(), primary_key=True),
    sa.Column('timestamp', sa.TIMESTAMP(timezone=True), index=True, default=sa.text('now()')),
    sa.Column('userid', sa.BigInteger(), sa.ForeignKey('users.id'), index=True),
    sa.Column('points', sa.BigInteger()),
)
