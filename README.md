# etsy-mcp-server

A [Model Context Protocol](https://modelcontextprotocol.io) server that exposes the
[Etsy Open API v3](https://developers.etsy.com/documentation/) as tools an MCP client
(Claude Desktop, Claude Code, etc.) can call.

## Features

Public (API key only):

- `find_shops`, `get_shop`, `get_shop_sections`, `get_shop_reviews`
- `search_active_listings`, `get_listing`, `get_listings_by_shop`,
  `get_listing_images`, `get_listing_inventory`
- `get_seller_taxonomy`, `get_taxonomy_properties`

Authenticated (require an OAuth access token):

- `get_authenticated_user`
- `create_draft_listing`, `update_listing`, `delete_listing`
- `get_shop_receipts`, `get_shop_receipt`, `create_receipt_shipment`

## Setup

### 1. Create an Etsy app

Register an app at the [Etsy Developers portal](https://www.etsy.com/developers/your-apps)
to get a **keystring** (API key). This is required for every request.

### 2. (Optional) Get an OAuth access token

Only needed for shop-management tools (creating/updating listings, reading receipts,
fetching the authenticated user). Etsy uses OAuth 2.0 with PKCE:

1. Generate a PKCE code verifier/challenge pair.
2. Send the shop owner to:
   ```
   https://www.etsy.com/oauth/connect?response_type=code&client_id=<API_KEY>&redirect_uri=<REDIRECT_URI>&scope=listings_r%20listings_w%20transactions_r&state=<STATE>&code_challenge=<CHALLENGE>&code_challenge_method=S256
   ```
3. Exchange the returned `code` for tokens:
   ```bash
   curl -X POST https://api.etsy.com/v3/public/oauth/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d grant_type=authorization_code \
     -d client_id=<API_KEY> \
     -d redirect_uri=<REDIRECT_URI> \
     -d code=<CODE> \
     -d code_verifier=<VERIFIER>
   ```
4. Save the returned `access_token` and `refresh_token`.

Full details: https://developers.etsy.com/documentation/essentials/authentication

Etsy access tokens expire after ~1 hour. This server automatically refreshes an expired
token using `ETSY_REFRESH_TOKEN` when a request comes back `401`, and logs the rotated
pair to stderr — update your stored env vars if you want the new refresh token to
survive a restart.

### 3. Configure environment variables

Copy `.env.example` to `.env` (or set these directly in your MCP client config):

```
ETSY_API_KEY=your_etsy_keystring_here
ETSY_ACCESS_TOKEN=   # optional, needed for authenticated tools
ETSY_REFRESH_TOKEN=  # optional, needed to auto-refresh the access token
```

### 4. Install and build

```bash
npm install
npm run build
```

## Usage with an MCP client

Example Claude Desktop / Claude Code config (`claude_desktop_config.json` or equivalent):

```json
{
  "mcpServers": {
    "etsy": {
      "command": "node",
      "args": ["/absolute/path/to/etsy-mcp-server/dist/index.js"],
      "env": {
        "ETSY_API_KEY": "your_etsy_keystring_here",
        "ETSY_ACCESS_TOKEN": "",
        "ETSY_REFRESH_TOKEN": ""
      }
    }
  }
}
```

Run standalone for debugging with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

## Development

```bash
npm run dev    # tsc --watch
npm run build  # one-off compile to dist/
```

The Etsy API wrapper lives in `src/etsy-client.ts`; MCP tool definitions live in
`src/index.ts`.
