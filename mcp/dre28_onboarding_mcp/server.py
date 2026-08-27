#!/usr/bin/env python3
"""Narrow onboarding MCP server for dre28.

This server intentionally exposes static onboarding and project-context tools
only. It does not provide shell, database, broker, filesystem proxy, filing,
donation, or credential operations.
"""
from __future__ import annotations

import argparse
import hmac
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from . import __version__

MAX_REQUEST_BYTES = 64_000
PROTOCOL_VERSION = "2025-03-26"
SERVER_NAME = "dre28-onboarding-mcp"
PROMPT_PATH = Path(__file__).with_name("onboarding_prompt.md")

COMMUNICATION_POLICY = {
    "frame_focus_finish": {
        "frame": "Establish context, source of truth, scope, constraints, and verified facts before acting.",
        "focus": "Convert the frame into decision-moving objectives and keep scope narrow.",
        "finish": "Deliver and verify the artifact, then report status, blocker, and next action.",
    },
    "listen_learn_lead": {
        "listen": "Preserve the principal's intent and preferences before changing work.",
        "learn": "Inspect current artifacts, sources, and prior decisions; refresh unstable facts.",
        "lead": "Execute the next authorized, high-leverage action without overclaiming.",
    },
}

PROJECT_BRIEF = {
    "project": "dre28",
    "purpose": "Pre-filing planning and website artifact support for a potential U.S. presidential campaign.",
    "repository": "https://github.com/ahill037/dre28",
    "intended_domain": "https://ayemane.com",
    "artifact_preference": "Durable HTML over Markdown for major planning and evidence artifacts.",
    "guardrails": [
        "Not legal advice.",
        "Do not invent filing, FEC, committee, treasurer, contribution, or launch facts.",
        "Use official or primary sources for compliance and public policy claims.",
        "Do not expose secrets, credentials, donor data, or private addresses.",
        "Do not create targeted political persuasion, demographic manipulation, or private-voter profiling workflows.",
    ],
    "platform_pillars": [
        "Empowerment through economic opportunity.",
        "Equality and accountability in law enforcement.",
        "Equip and empower the military, teachers, students, and allies.",
        "Reduce the federal budget's reliance on debt.",
    ],
}


def _read_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _json_default(obj: Any) -> str:
    return str(obj)


def _dump(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, default=_json_default)


def _markdown_project_brief() -> str:
    lines = [
        "# dre28 Project Brief",
        "",
        f"- Project: `{PROJECT_BRIEF['project']}`",
        f"- Purpose: {PROJECT_BRIEF['purpose']}",
        f"- Repository: {PROJECT_BRIEF['repository']}",
        f"- Intended domain: {PROJECT_BRIEF['intended_domain']}",
        f"- Artifact preference: {PROJECT_BRIEF['artifact_preference']}",
        "",
        "## Guardrails",
    ]
    lines.extend(f"- {item}" for item in PROJECT_BRIEF["guardrails"])
    lines.extend(["", "## Platform Pillars"])
    lines.extend(f"- {item}" for item in PROJECT_BRIEF["platform_pillars"])
    return "\n".join(lines)


TOOLS: dict[str, dict[str, Any]] = {
    "dre28_get_onboarding_prompt": {
        "description": "Return the dre28 onboarding prompt using DreAnalytica Frame/Focus/Finish and Listen/Learn/Lead.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["markdown", "json"],
                    "default": "markdown",
                }
            },
            "additionalProperties": False,
        },
    },
    "dre28_get_project_brief": {
        "description": "Return a concise project brief, public anchors, platform pillars, and guardrails.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["markdown", "json"],
                    "default": "markdown",
                }
            },
            "additionalProperties": False,
        },
    },
    "dre28_get_communication_policy": {
        "description": "Return the DreAnalytica communication policy framing used by dre28 onboarding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["markdown", "json"],
                    "default": "markdown",
                }
            },
            "additionalProperties": False,
        },
    },
    "dre28_health": {
        "description": "Return service health and version metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
}


def tool_descriptors() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "description": spec["description"],
            "inputSchema": spec["inputSchema"],
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
        }
        for name, spec in TOOLS.items()
    ]


def _format_policy_markdown() -> str:
    fff = COMMUNICATION_POLICY["frame_focus_finish"]
    lll = COMMUNICATION_POLICY["listen_learn_lead"]
    return "\n".join(
        [
            "# DreAnalytica Communication Policy",
            "",
            "## Frame, Focus, And Finish",
            f"- Frame: {fff['frame']}",
            f"- Focus: {fff['focus']}",
            f"- Finish: {fff['finish']}",
            "",
            "## Listen, Learn, And Lead",
            f"- Listen: {lll['listen']}",
            f"- Learn: {lll['learn']}",
            f"- Lead: {lll['lead']}",
        ]
    )


class MCPApplication:
    def call_tool(self, name: str, args: dict[str, Any]) -> Any:
        if name not in TOOLS:
            raise ValueError("unknown tool")
        allowed = set(TOOLS[name]["inputSchema"].get("properties", {}))
        unexpected = sorted(set(args) - allowed)
        if unexpected:
            raise ValueError(f"unexpected arguments: {', '.join(unexpected)}")
        fmt = args.get("format", "markdown")
        if fmt not in {"markdown", "json"}:
            raise ValueError("format must be 'markdown' or 'json'")

        if name == "dre28_get_onboarding_prompt":
            prompt = _read_prompt()
            if fmt == "json":
                return {"prompt": prompt}
            return prompt
        if name == "dre28_get_project_brief":
            if fmt == "json":
                return PROJECT_BRIEF
            return _markdown_project_brief()
        if name == "dre28_get_communication_policy":
            if fmt == "json":
                return COMMUNICATION_POLICY
            return _format_policy_markdown()
        if name == "dre28_health":
            return {
                "status": "ok",
                "server": SERVER_NAME,
                "version": __version__,
                "tools": sorted(TOOLS),
            }
        raise AssertionError(name)

    def handle(self, request: dict[str, Any]) -> dict[str, Any] | None:
        method = request.get("method")
        request_id = request.get("id")
        if request_id is None:
            return None
        try:
            if method == "initialize":
                result = {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": SERVER_NAME, "version": __version__},
                }
            elif method == "tools/list":
                result = {"tools": tool_descriptors()}
            elif method == "tools/call":
                params = request.get("params", {})
                if not isinstance(params, dict):
                    raise ValueError("params must be an object")
                output = self.call_tool(
                    str(params.get("name", "")),
                    params.get("arguments") or {},
                )
                text = output if isinstance(output, str) else _dump(output)
                result = {
                    "content": [{"type": "text", "text": text}],
                    "structuredContent": output if isinstance(output, dict) else {"text": output},
                    "isError": False,
                }
            elif method == "ping":
                result = {}
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": "Method not found"},
                }
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except (OSError, ValueError, TypeError) as exc:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": str(exc)},
            }


def make_handler(app: MCPApplication, token: str):
    class Handler(BaseHTTPRequestHandler):
        server_version = "DRE28OnboardingMCP/0.1"

        def log_message(self, fmt: str, *args: Any) -> None:
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

        def _json(self, status: int, payload: dict[str, Any] | None) -> None:
            encoded = b"" if payload is None else json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            if encoded:
                self.wfile.write(encoded)

        def do_GET(self) -> None:
            if self.path != "/healthz":
                self._json(404, {"error": "not found"})
                return
            self._json(
                200,
                {
                    "status": "ok",
                    "server": SERVER_NAME,
                    "version": __version__,
                    "endpoint": "/mcp",
                    "auth": "bearer",
                },
            )

        def do_POST(self) -> None:
            if self.path != "/mcp":
                self._json(404, {"error": "not found"})
                return
            supplied = self.headers.get("Authorization", "")
            if not supplied.startswith("Bearer ") or not hmac.compare_digest(
                supplied[7:], token
            ):
                self._json(401, {"error": "authentication required"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._json(400, {"error": "invalid content length"})
                return
            if length <= 0 or length > MAX_REQUEST_BYTES:
                self._json(413, {"error": "request payload rejected"})
                return
            try:
                request = json.loads(self.rfile.read(length))
                if not isinstance(request, dict):
                    raise ValueError
            except (json.JSONDecodeError, ValueError):
                self._json(400, {"error": "invalid JSON-RPC request"})
                return
            response = app.handle(request)
            self._json(202 if response is None else 200, response)

    return Handler


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="dre28 onboarding MCP server")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        choices=["127.0.0.1", "localhost"],
        help="Localhost binding only.",
    )
    parser.add_argument("--port", type=int, default=8790)
    args = parser.parse_args(argv)

    token = os.environ.get("DRE28_MCP_AUTH_TOKEN", "")
    if len(token) < 32:
        parser.error("DRE28_MCP_AUTH_TOKEN must be set to at least 32 characters")

    server = ThreadingHTTPServer((args.host, args.port), make_handler(MCPApplication(), token))
    print(f"{SERVER_NAME} listening on http://{args.host}:{args.port}/mcp", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

