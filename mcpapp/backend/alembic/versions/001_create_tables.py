"""create tables

Revision ID: 001
Revises: 
Create Date: 2024-03-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 创建消息表
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment="主键ID"),
        sa.Column('session_id', sa.Integer(), nullable=False, comment="会话ID"),
        sa.Column('message_type', sa.String(length=50), nullable=False, comment="消息类型(user/assistant/system)"),
        sa.Column('content', sa.Text(), nullable=False, comment="消息内容"),
        sa.Column('message_metadata', sa.JSON(), nullable=True, comment="消息元数据"),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment="创建时间"),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment="更新时间"),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1'), comment="是否有效"),
        sa.ForeignKeyConstraint(['session_id'], ['chat_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_session_id', 'messages', ['session_id'])

def downgrade():
    op.drop_table('messages') 