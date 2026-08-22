# Test

A minimal Node.js client for the [Etsy Open API v3](https://developer.etsy.com/documentation/) (`api.etsy.com`).

## Setup

```sh
cp .env.example .env
# fill in ETSY_API_KEY (and optionally ETSY_ACCESS_TOKEN) in .env
```

## Usage

```js
import { EtsyClient } from "./src/etsyClient.js";

const client = new EtsyClient({ apiKey: process.env.ETSY_API_KEY });

const pong = await client.ping();
const shop = await client.getShop(12345678);
const listing = await client.getListing(87654321);
```

Run the example script (requires `ETSY_API_KEY` to be set):

```sh
export ETSY_API_KEY=your-etsy-keystring
npm run example -- "some shop name"
```

## Notes

- All requests to `api.etsy.com` require an API key (`x-api-key` header), issued when you register an app at [Etsy Developers](https://www.etsy.com/developers/register).
- Endpoints scoped to a specific shop/user (creating listings, reading orders, etc.) additionally require an OAuth 2.0 access token — set `ETSY_ACCESS_TOKEN` once you've completed Etsy's OAuth flow.
