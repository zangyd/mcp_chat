"""rename metadata columns

Revision ID: 002
Revises: 001
Create Date: 2024-03-20 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # 修改 chat_messages 表中的 metadata 列名
    op.alter_column('chat_messages', 'metadata',
                    new_column_name='message_metadata',
                    existing_type=sa.JSON(),
                    existing_nullable=True)

    # 修改 mcp_servers 表中的 metadata 列名
    op.alter_column('mcp_servers', 'metadata',
                    new_column_name='server_metadata',
                    existing_type=sa.JSON(),
                    existing_nullable=True)

    # 修改 server_calls 表中的 metadata 列名（如果存在）
    try:
        op.alter_column('server_calls', 'metadata',
                    new_column_name='call_metadata',
                    existing_type=sa.JSON(),
                    existing_nullable=True)
    except:
        pass

def downgrade():
    # 还原 chat_messages 表中的列名
    op.alter_column('chat_messages', 'message_metadata',
                    new_column_name='metadata',
                    existing_type=sa.JSON(),
                    existing_nullable=True)

    # 还原 mcp_servers 表中的列名
    op.alter_column('mcp_servers', 'server_metadata',
                    new_column_name='metadata',
                    existing_type=sa.JSON(),
                    existing_nullable=True)

    # 还原 server_calls 表中的列名（如果存在）
    try:
        op.alter_column('server_calls', 'call_metadata',
                    new_column_name='metadata',
                    existing_type=sa.JSON(),
                    existing_nullable=True)
    except:
        pass 