from typing import Dict, List, Optional
from app.core.config import settings

class MCPServerSelector:
    def __init__(self):
        self.server_capabilities = {
            "mysql": ["数据库操作", "SQL查询", "数据分析"],
            "filesystem": ["文件操作", "目录管理", "文件搜索"],
            "hello_world": ["基础测试", "示例功能"]
        }
        
        self.server_priorities = {
            "mysql": 1,
            "filesystem": 1,
            "hello_world": 2
        }

    async def select_server(self, required_tools: List[str], user_context: Optional[Dict] = None) -> List[Dict]:
        """
        根据所需工具和用户上下文选择合适的MCP服务器
        返回按优先级排序的服务器列表
        """
        matched_servers = []
        
        for server_name, capabilities in self.server_capabilities.items():
            # 检查服务器是否提供所需的工具
            if any(tool in capabilities for tool in required_tools):
                server_info = {
                    "name": server_name,
                    "priority": self.server_priorities.get(server_name, 99),
                    "capabilities": capabilities,
                    "matched_tools": [tool for tool in required_tools if tool in capabilities]
                }
                matched_servers.append(server_info)
        
        # 按优先级排序
        matched_servers.sort(key=lambda x: x["priority"])
        return matched_servers

    async def get_server_status(self, server_name: str) -> Dict:
        """获取服务器状态信息"""
        # 这里可以实现实际的服务器状态检查逻辑
        return {
            "name": server_name,
            "status": "active",
            "load": 0.5,  # 示例负载值
            "response_time": 100  # 示例响应时间（毫秒）
        }

    async def validate_server(self, server_name: str) -> bool:
        """验证服务器是否可用"""
        status = await self.get_server_status(server_name)
        return status["status"] == "active"