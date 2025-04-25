import os
import logging
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db_config():
    """从环境变量获取数据库配置信息

    返回:
        dict: 包含数据库连接所需的配置信息
        - host: 数据库主机地址
        - port: 数据库端口
        - user: 数据库用户名
        - password: 数据库密码
        - database: 数据库名称
        - role: 数据库角色权限

    异常:
        ValueError: 当必需的配置信息缺失时抛出
    """
    # 加载.env文件（如果存在）
    load_dotenv()

    # 默认配置
    default_config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "Autotest@2024",
        "database": "mcp_chat",
        "role": "admin"
    }

    # 从环境变量获取配置，如果环境变量不存在则使用默认值
    config = {
        "host": os.getenv("MYSQL_HOST", default_config["host"]),
        "port": int(os.getenv("MYSQL_PORT", default_config["port"])),
        "user": os.getenv("MYSQL_USER", default_config["user"]),
        "password": os.getenv("MYSQL_PASSWORD", default_config["password"]),
        "database": os.getenv("MYSQL_DATABASE", default_config["database"]),
        "role": os.getenv("MYSQL_ROLE", default_config["role"])
    }
    
    logger.debug(f"数据库配置: {config}")
    return config

# 定义角色权限
ROLE_PERMISSIONS = {
    "readonly": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN"],  # 只读权限
    "writer": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "INSERT", "UPDATE", "DELETE"],  # 读写权限
    "admin": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "INSERT", "UPDATE", "DELETE", 
             "CREATE", "ALTER", "DROP", "TRUNCATE", "CREATE VIEW", "SHOW VIEW", "CREATE PROCEDURE", "ALTER PROCEDURE", "DROP PROCEDURE", "CREATE EVENT", "ALTER EVENT", "DROP EVENT", "CREATE TRIGGER", "ALTER TRIGGER", "DROP TRIGGER", "CREATE USER", "ALTER USER", "DROP USER", "CREATE ROLE", "ALTER ROLE", "DROP ROLE", "GRANT", "REVOKE", "LOCK TABLES", "UNLOCK TABLES", "CREATE DATABASE", "ALTER DATABASE", "DROP DATABASE", "CREATE TABLE", "ALTER TABLE", "DROP TABLE", "CREATE INDEX", "ALTER INDEX", "DROP INDEX", "CREATE VIEW", "ALTER VIEW", "DROP VIEW", "CREATE USER", "ALTER USER", "DROP USER", "CREATE ROLE", "ALTER ROLE", "DROP ROLE", "GRANT", "REVOKE","USE"]  # 管理员权限
}

def get_role_permissions(role: str) -> list:
    """获取指定角色的权限列表
    
    参数:
        role (str): 角色名称
        
    返回:
        list: 该角色允许执行的SQL操作列表
    """
    permissions = ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS["readonly"])  # 默认返回只读权限
    logger.debug(f"角色 {role} 的权限: {permissions}")
    return permissions