import asyncio
import uvicorn

from typing import Sequence
from mcp.server.sse import SseServerTransport

from mcp.server import Server
from mcp.types import  Tool, TextContent

from starlette.applications import Starlette
from starlette.routing import Route, Mount

from handles.base import ToolRegistry

# 初始化服务器
app = Server("operateMysql")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
        列出所有可用的MySQL操作工具
    """
    return ToolRegistry.get_all_tools()

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    """调用指定的工具执行操作
    
    Args:
        name (str): 工具名称
        arguments (dict): 工具参数

    Returns:
        Sequence[TextContent]: 工具执行结果

    Raises:
        ValueError: 当指定了未知的工具名称时抛出异常
    """
    tool = ToolRegistry.get_tool(name)

    return await tool.run_tool(arguments)


async def run_stdio():
    """运行标准输入输出模式的服务器
    
    使用标准输入输出流(stdio)运行服务器，主要用于命令行交互模式
    
    Raises:
        Exception: 当服务器运行出错时抛出异常
    """
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        except Exception as e:
            print(f"服务器错误: {str(e)}")
            raise

def run_sse():
    """运行SSE(Server-Sent Events)模式的服务器
    
    启动一个支持SSE的Web服务器，允许客户端通过HTTP长连接接收服务器推送的消息
    服务器默认监听0.0.0.0:9000
    """
    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        """处理SSE连接请求
        
        Args:
            request: HTTP请求对象
        """
        async with sse.connect_sse(
                request.scope, request.receive, request._send
        ) as streams:
            await app.run(streams[0], streams[1], app.create_initialization_options())

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message)
        ],
    )
    uvicorn.run(starlette_app, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    import sys

    # 根据命令行参数选择启动模式
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # 标准输入输出模式
        asyncio.run(run_stdio())
    else:
        # 默认 SSE 模式
        run_sse()
