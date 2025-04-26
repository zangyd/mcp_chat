# MCP Chat 数据库结构文档

## 表结构概览

数据库名：`mcp_chat`

包含以下表：
- chat_messages：聊天消息表
- chat_sessions：聊天会话表
- mcp_servers：MCP服务器信息表
- server_calls：服务器调用记录表
- users：用户表
- alembic_version：数据库版本控制表

## 详细表结构

### 1. chat_messages（聊天消息表）

| 字段名           | 类型                              | 空值 | 键   | 默认值            | 额外说明                    |
|-----------------|----------------------------------|------|------|------------------|---------------------------|
| id              | int                              | NO   | PRI  | NULL            | 自增主键                    |
| session_id      | int                              | NO   | MUL  | NULL            | 关联chat_sessions表的外键    |
| message_type    | enum('user','assistant','system')| NO   | MUL  | NULL            | 消息类型                    |
| content         | text                             | NO   |      | NULL            | 消息内容                    |
| message_metadata| json                             | YES  |      | NULL            | 消息元数据                  |
| created_at      | datetime                         | NO   |      | CURRENT_TIMESTAMP| 创建时间                    |
| updated_at      | datetime                         | NO   |      | CURRENT_TIMESTAMP| 更新时间，自动更新            |
| is_active       | tinyint(1)                       | NO   |      | 1               | 是否有效                    |

### 2. chat_sessions（聊天会话表）

| 字段名        | 类型          | 空值 | 键   | 默认值            | 额外说明                    |
|--------------|--------------|------|------|------------------|---------------------------|
| id           | int          | NO   | PRI  | NULL            | 自增主键                    |
| title        | varchar(200) | NO   |      | NULL            | 会话标题                    |
| user_id      | int          | NO   | MUL  | NULL            | 关联users表的外键           |
| session_data | json         | YES  |      | NULL            | 会话相关数据                |
| created_at   | datetime     | NO   |      | CURRENT_TIMESTAMP| 创建时间                    |
| updated_at   | datetime     | NO   |      | CURRENT_TIMESTAMP| 更新时间，自动更新            |
| is_active    | tinyint(1)   | NO   |      | 1               | 是否有效                    |

### 3. mcp_servers（MCP服务器信息表）

| 字段名          | 类型                                    | 空值 | 键   | 默认值            | 额外说明                    |
|----------------|----------------------------------------|------|------|------------------|---------------------------|
| id             | int                                    | NO   | PRI  | NULL            | 自增主键                    |
| name           | varchar(100)                           | NO   |      | NULL            | 服务器名称                  |
| description    | text                                   | YES  |      | NULL            | 服务器描述                  |
| host           | varchar(200)                           | NO   | MUL  | NULL            | 服务器地址                  |
| port           | int                                    | NO   |      | NULL            | 服务器端口                  |
| status         | enum('online','offline','maintenance') | YES  | MUL  | offline         | 服务器状态                  |
| capabilities   | json                                   | YES  |      | NULL            | 服务器能力描述              |
| server_metadata| json                                   | YES  |      | NULL            | 服务器元数据                |
| response_time  | float                                  | YES  |      | NULL            | 平均响应时间(ms)            |
| success_rate   | float                                  | YES  |      | NULL            | 成功率                     |
| server_load    | float                                  | YES  |      | NULL            | 负载情况                    |
| created_at     | datetime                               | NO   |      | CURRENT_TIMESTAMP| 创建时间                    |
| updated_at     | datetime                               | NO   |      | CURRENT_TIMESTAMP| 更新时间，自动更新            |

### 4. server_calls（服务器调用记录表）

| 字段名         | 类型                                              | 空值 | 键   | 默认值            | 额外说明                    |
|---------------|--------------------------------------------------|------|------|------------------|---------------------------|
| id            | int                                              | NO   | PRI  | NULL            | 自增主键                    |
| server_id     | int                                              | NO   | MUL  | NULL            | 关联mcp_servers表的外键     |
| session_id    | int                                              | NO   | MUL  | NULL            | 关联chat_sessions表的外键   |
| message_id    | int                                              | NO   | MUL  | NULL            | 关联chat_messages表的外键   |
| request_data  | json                                             | NO   |      | NULL            | 请求数据                    |
| response_data | json                                             | YES  |      | NULL            | 响应数据                    |
| status        | enum('success','failed','timeout','in_progress') | NO   | MUL  | NULL            | 调用状态                    |
| error_message | text                                             | YES  |      | NULL            | 错误信息                    |
| response_time | float                                            | YES  |      | NULL            | 响应时间(ms)               |
| created_at    | datetime                                         | NO   |      | CURRENT_TIMESTAMP| 创建时间                    |
| updated_at    | datetime                                         | NO   |      | CURRENT_TIMESTAMP| 更新时间，自动更新            |

### 5. users（用户表）

| 字段名           | 类型          | 空值 | 键   | 默认值            | 额外说明                    |
|-----------------|--------------|------|------|------------------|---------------------------|
| id              | int          | NO   | PRI  | NULL            | 自增主键                    |
| username        | varchar(50)  | NO   | UNI  | NULL            | 用户名，唯一                 |
| email           | varchar(100) | NO   | UNI  | NULL            | 邮箱，唯一                  |
| hashed_password | varchar(200) | NO   |      | NULL            | 加密后的密码                |
| is_active       | tinyint(1)   | YES  |      | 1               | 是否激活                    |
| is_superuser    | tinyint(1)   | YES  |      | 0               | 是否是超级用户              |
| avatar          | varchar(200) | YES  |      | NULL            | 头像URL                    |
| phone           | varchar(20)  | YES  | UNI  | NULL            | 手机号，唯一                |
| full_name       | varchar(100) | YES  |      | NULL            | 全名                      |
| created_at      | datetime     | NO   |      | CURRENT_TIMESTAMP| 创建时间                    |
| updated_at      | datetime     | NO   |      | CURRENT_TIMESTAMP| 更新时间，自动更新            |

## 表关系

1. chat_messages 表：
   - session_id -> chat_sessions.id (多对一)

2. chat_sessions 表：
   - user_id -> users.id (多对一)

3. server_calls 表：
   - server_id -> mcp_servers.id (多对一)
   - session_id -> chat_sessions.id (多对一)
   - message_id -> chat_messages.id (多对一)

## 注意事项

1. 所有表都包含 created_at 和 updated_at 字段，用于记录创建和更新时间
2. 大多数表都包含 is_active 字段，用于软删除功能
3. 敏感字段（如密码）都经过加密处理
4. 使用枚举类型限制特定字段的值范围
5. 适当使用索引提高查询性能
6. JSON类型字段用于存储灵活的结构化数据 