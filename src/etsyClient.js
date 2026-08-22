const BASE_URL = "https://api.etsy.com/v3/application";

/**
 * Minimal client for the Etsy Open API v3.
 * All requests require an API key; endpoints scoped to a specific user/shop
 * additionally require an OAuth access token obtained via Etsy's OAuth 2.0 flow.
 */
export class EtsyClient {
  constructor({ apiKey, accessToken } = {}) {
    if (!apiKey) {
      throw new Error("EtsyClient requires an apiKey");
    }
    this.apiKey = apiKey;
    this.accessToken = accessToken;
  }

  async request(method, path, { params, body } = {}) {
    const url = new URL(BASE_URL + path);
    if (params) {
      for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== null) {
          url.searchParams.set(key, value);
        }
      }
    }

    const headers = { "x-api-key": this.apiKey };
    if (this.accessToken) {
      headers.Authorization = `Bearer ${this.accessToken}`;
    }
    if (body) {
      headers["Content-Type"] = "application/json";
    }

    const response = await fetch(url, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    const data = await response.json().catch(() => undefined);
    if (!response.ok) {
      const message = data?.error || data?.message || response.statusText;
      throw new Error(`Etsy API ${method} ${path} failed (${response.status}): ${message}`);
    }
    return data;
  }

  /** Verifies API key connectivity. */
  ping() {
    return this.request("GET", "/openapi-ping");
  }

  /** Fetches a shop by its numeric shop ID. */
  getShop(shopId) {
    return this.request("GET", `/shops/${shopId}`);
  }

  /** Searches for shops by name. */
  findShops(shopName, { limit, offset } = {}) {
    return this.request("GET", "/shops", { params: { shop_name: shopName, limit, offset } });
  }

  /** Fetches a single listing by its numeric listing ID. */
  getListing(listingId) {
    return this.request("GET", `/listings/${listingId}`);
  }

  /** Fetches active listings for a shop. */
  getShopListings(shopId, { limit, offset, state = "active" } = {}) {
    return this.request("GET", `/shops/${shopId}/listings`, { params: { limit, offset, state } });
  }
}

export default EtsyClient;
