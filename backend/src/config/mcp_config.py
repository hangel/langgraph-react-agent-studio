import os
from typing import Any, Dict, Optional

from pydantic import BaseModel


class MCPServerConfig(BaseModel):
    """Configuration for a single MCP server."""

    name: str
    transport: str  # "stdio" or "streamable_http"
    command: Optional[str] = None
    args: Optional[list[str]] = None
    url: Optional[str] = None
    enabled: bool = True


class MCPConfiguration:
    """Central configuration for all MCP servers."""

    @classmethod
    def get_default_servers(cls) -> Dict[str, Dict[str, Any]]:
        """Get default MCP server configurations."""
        return {
            "filesystem": {
                "transport": "stdio",
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    os.getenv("MCP_FILESYSTEM_PATH", "/tmp"),
                ],
                "enabled": os.getenv("MCP_FILESYSTEM_ENABLED", "false").lower()
                == "true",
            },
            "brave_search": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "enabled": os.getenv("MCP_BRAVE_SEARCH_ENABLED", "false").lower()
                == "true",
                "env": {
                    "BRAVE_API_KEY": os.getenv("BRAVE_API_KEY"),
                },
            },
        }
