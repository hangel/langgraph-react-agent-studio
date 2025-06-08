import asyncio
import logging
from typing import List

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from config.mcp_config import MCPConfiguration

logger = logging.getLogger(__name__)


async def load_mcp_tools() -> List[BaseTool]:
    """Load tools from configured MCP servers.

    Returns:
        List of LangChain tools from MCP servers
    """
    server_configs = MCPConfiguration.get_default_servers()
    enabled_configs = {
        name: config
        for name, config in server_configs.items()
        if config.get("enabled", True)
    }

    if not enabled_configs:
        logger.info("No MCP servers enabled, returning empty tool list")
        return []

    try:
        client = MultiServerMCPClient(enabled_configs)
        tools = await client.get_tools()
        logger.info(
            f"Loaded {len(tools)} tools from {len(enabled_configs)} MCP servers"
        )
        return tools
    except Exception as e:
        logger.error(f"Failed to load MCP tools: {e}")
        return []


def get_mcp_tools_sync() -> List[BaseTool]:
    """Synchronous wrapper for loading MCP tools."""
    try:
        return asyncio.run(load_mcp_tools())
    except Exception as e:
        logger.error(f"Failed to load MCP tools synchronously: {e}")
        return []
