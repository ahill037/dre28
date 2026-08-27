#!/usr/bin/env python3
"""In-process smoke checks for the dre28 onboarding MCP application."""
from __future__ import annotations

from dre28_onboarding_mcp.server import MCPApplication


def main() -> None:
    app = MCPApplication()
    init = app.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    assert init and init["result"]["serverInfo"]["name"] == "dre28-onboarding-mcp"

    tools = app.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    names = {tool["name"] for tool in tools["result"]["tools"]}
    assert "dre28_get_onboarding_prompt" in names
    assert "dre28_get_communication_policy" in names

    prompt = app.handle(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "dre28_get_onboarding_prompt", "arguments": {}},
        }
    )
    text = prompt["result"]["content"][0]["text"]
    assert "Frame, Focus, And Finish" in text
    assert "Listen, Learn, And Lead" in text

    health = app.handle(
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "dre28_health", "arguments": {}},
        }
    )
    assert health["result"]["structuredContent"]["status"] == "ok"
    print("smoke: ok")


if __name__ == "__main__":
    main()

