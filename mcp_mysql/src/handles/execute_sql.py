from typing import Dict, Any, Sequence
import logging
import traceback

from mcp import Tool
from mcp.types import TextContent
from mysql.connector import connect, Error

from config import get_db_config, get_role_permissions
from .base import BaseHandler

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ExecuteSQL(BaseHandler):
    name = "execute_sql"
    description = (
        "在MySQL数据库上执行SQL (multiple SQL execution, separated by ';')"
    )

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要执行的SQL语句"
                    }
                },
                "required": ["query"]
            }
        )

    def check_sql_permission(self, sql: str, allowed_operations: list) -> bool:
        """检查SQL语句是否有执行权限
        
        参数:
            sql (str): SQL语句
            allowed_operations (list): 允许的操作列表
            
        返回:
            bool: 是否有权限执行
        """
        # 提取SQL语句的操作类型
        operation = sql.strip().split()[0].upper()
        return operation in allowed_operations

    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
       """执行SQL查询语句

          参数:
              query (str): 要执行的SQL语句，支持多条语句以分号分隔

          返回:
              list[TextContent]: 包含查询结果的TextContent列表
              - 对于SELECT查询：返回CSV格式的结果，包含列名和数据
              - 对于SHOW TABLES：返回数据库中的所有表名
              - 对于其他查询：返回执行状态和影响行数
              - 多条语句的结果以"---"分隔

          异常:
              Error: 当数据库连接或查询执行失败时抛出
          """
       try:
           config = get_db_config()
           logger.debug(f"数据库配置: {config}")
           
           if "query" not in arguments:
               raise ValueError("缺少查询语句")

           query = arguments["query"]
           logger.debug(f"执行SQL: {query}")
           
           # 获取角色权限
           allowed_operations = get_role_permissions(config["role"])
           logger.debug(f"允许的操作: {allowed_operations}")

           try:
               with connect(**{k: v for k, v in config.items() if k != "role"}) as conn:
                   logger.debug("数据库连接成功")
                   with conn.cursor() as cursor:
                       statements = [stmt.strip() for stmt in query.split(';') if stmt.strip()]
                       results = []

                       for statement in statements:
                           try:
                               # 检查权限
                               if not self.check_sql_permission(statement, allowed_operations):
                                   error_msg = f"权限不足: 当前角色 '{config['role']}' 无权执行该SQL操作"
                                   logger.warning(error_msg)
                                   results.append(error_msg)
                                   continue

                               cursor.execute(statement)
                               logger.debug(f"执行成功: {statement}")

                               # 检查语句是否返回了结果集 (SELECT, SHOW, EXPLAIN, etc.)
                               if cursor.description:
                                   columns = [desc[0] for desc in cursor.description]
                                   rows = cursor.fetchall()
                                   logger.debug(f"查询结果: {len(rows)} 行")

                                   # 将每一行的数据转换为字符串，特殊处理None值
                                   formatted_rows = []
                                   for row in rows:
                                       formatted_row = ["NULL" if value is None else str(value) for value in row]
                                       formatted_rows.append(",".join(formatted_row))

                                   # 将列名和数据合并为CSV格式
                                   results.append("\n".join([",".join(columns)] + formatted_rows))

                               # 如果语句没有返回结果集 (INSERT, UPDATE, DELETE, etc.)
                               else:
                                   conn.commit()  # 只有在非查询语句时才提交
                                   success_msg = f"查询执行成功。影响行数: {cursor.rowcount}"
                                   logger.info(success_msg)
                                   results.append(success_msg)

                           except Error as stmt_error:
                               # 单条语句执行出错时，记录错误并继续执行
                               error_msg = f"执行语句 '{statement}' 出错: {str(stmt_error)}"
                               logger.error(error_msg)
                               logger.error(traceback.format_exc())
                               results.append(error_msg)
                               # 可以在这里选择是否继续执行后续语句，目前是继续

                   return [TextContent(type="text", text="\n---\n".join(results))]

           except Error as e:
               error_msg = f"数据库连接失败: {str(e)}"
               logger.error(error_msg)
               logger.error(traceback.format_exc())
               return [TextContent(type="text", text=error_msg)]

       except Exception as e:
           error_msg = f"未知错误: {str(e)}"
           logger.error(error_msg)
           logger.error(traceback.format_exc())
           return [TextContent(type="text", text=error_msg)]

