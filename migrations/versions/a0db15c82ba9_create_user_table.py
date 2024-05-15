"""create user table

Revision ID: a0db15c82ba9
Revises: 
Create Date: 2024-05-15 19:57:38.414880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a0db15c82ba9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
                    sa.Column('first_name', sa.String(length=48), nullable=False),
                    sa.Column('last_name', sa.String(length=72), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('username', sa.String(length=24), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column('salt', sa.String(length=255), nullable=False),
                    sa.Column('disabled', sa.Boolean(), nullable=True),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.Column('otp_validation_token', sa.String(length=255), nullable=True),
                    sa.Column('otp_secret', sa.String(length=255), nullable=True),
                    sa.Column('mail_validation_token', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.PrimaryKeyConstraint('id', name='user_pkey'),
                    sa.UniqueConstraint('email', name='user_email_key'),
                    sa.UniqueConstraint('mail_validation_token', name='mail_validation_token_key'),
                    sa.UniqueConstraint('otp_secret'),
                    sa.UniqueConstraint('otp_validation_token', name='otp_validation_token_key'),
                    sa.UniqueConstraint('salt', name='user_salt_key'),
                    sa.UniqueConstraint('username', name='user_username_key')
                    )


def downgrade() -> None:
    op.drop_table('user')
