
opencode2api common

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode2api/deepseek-v4-flash",
  "mcp": {

  },
  "provider": {
    "opencode2api": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "opencode2api (local)",
      "options": {
        "baseURL": "http://localhost:8000/v1",
        "apiKey": "public"
      },
      "models": {
        "deepseek-v4-flash": { "name": "DeepSeek V4 Flash" },
        "mimo-v2.5": { "name": "Mimo 2.5" },
        "ling-3.0-flash": { "name": "Ling 3.0 Flash" },
        "nemotron-3-ultra": { "name": "Nemotron 3 Ultra" },
        "north-mini-code": { "name": "North Mini Code" },
        "laguna-s-2.1": { "name": "Laguna S 2.1" },
        "longcat-2.0": { "name": "Longcat 2.0" }
      }
    }
  }
}
```


IDA Pro MCP

```json
    "ida-pro": {
      "type": "remote",
      "url": "http://127.0.0.1:13337/mcp",
      "enabled": true
    }
```


Brawser use MCP

```json
    "chrome-devtools": {
      "type": "local",
      "command": ["npx", "-y", "chrome-devtools-mcp@latest", "--experimentalScreencast=true"],
      "enabled": true
    }
```

-------------------

