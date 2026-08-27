# dre28 Onboarding MCP

- Status: draft v1
- Host target: GX10
- Default bind: `127.0.0.1:8790`
- Transport: HTTP JSON-RPC endpoint at `/mcp`
- Auth: bearer token from `DRE28_MCP_AUTH_TOKEN`

## Purpose

- Serve the `dre28` onboarding prompt and operating brief through a narrow MCP-style interface.
- Keep the server coordination/onboarding-only.
- Avoid DB, broker, shell, arbitrary filesystem, campaign-filing mutation, donation processing, or credential exposure.

## Tools

- `dre28_get_onboarding_prompt`
- `dre28_get_project_brief`
- `dre28_get_communication_policy`
- `dre28_health`

## Local Run

```bash
export DRE28_MCP_AUTH_TOKEN="<32+ character token>"
python3 -m dre28_onboarding_mcp.server --host 127.0.0.1 --port 8790
```

## Health Check

```bash
curl http://127.0.0.1:8790/healthz
```

## MCP Smoke Test

```bash
curl -sS http://127.0.0.1:8790/mcp \
  -H "Authorization: Bearer $DRE28_MCP_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## Client Config Shape

```json
{
  "mcpServers": {
    "dre28-onboarding-gx10": {
      "type": "http",
      "url": "http://127.0.0.1:8790/mcp",
      "headers": {
        "Authorization": "Bearer ${DRE28_MCP_AUTH_TOKEN}"
      }
    }
  }
}
```

