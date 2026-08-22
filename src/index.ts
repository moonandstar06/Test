#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { EtsyApiError, EtsyClient } from "./etsy-client.js";

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

const client = new EtsyClient({
  apiKey: requireEnv("ETSY_API_KEY"),
  accessToken: process.env.ETSY_ACCESS_TOKEN || undefined,
  refreshToken: process.env.ETSY_REFRESH_TOKEN || undefined,
  baseUrl: process.env.ETSY_API_BASE_URL || undefined,
  onTokenRefresh: ({ accessToken, refreshToken }) => {
    // Etsy access tokens are short-lived (~1h). We keep the refreshed pair
    // in memory for the lifetime of this process; log to stderr so the
    // operator can persist it if they want long-running credentials.
    process.env.ETSY_ACCESS_TOKEN = accessToken;
    process.env.ETSY_REFRESH_TOKEN = refreshToken;
    console.error(
      "[etsy-mcp-server] OAuth access token refreshed. Update your stored ETSY_REFRESH_TOKEN if it changed:",
      refreshToken,
    );
  },
});

const server = new McpServer({
  name: "etsy-mcp-server",
  version: "0.1.0",
});

function textResult(data: unknown) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }],
  };
}

function errorResult(err: unknown) {
  const message =
    err instanceof EtsyApiError
      ? `Etsy API error (${err.status}): ${err.message}\n${JSON.stringify(err.body)}`
      : err instanceof Error
        ? err.message
        : String(err);
  return {
    isError: true as const,
    content: [{ type: "text" as const, text: message }],
  };
}

async function handle<T>(fn: () => Promise<T>) {
  try {
    return textResult(await fn());
  } catch (err) {
    return errorResult(err);
  }
}

// ---------------------------------------------------------------------------
// Shops
// ---------------------------------------------------------------------------

server.registerTool(
  "find_shops",
  {
    title: "Find Etsy shops",
    description: "Search for Etsy shops by name.",
    inputSchema: {
      shop_name: z.string().describe("Shop name or partial name to search for"),
      limit: z.number().int().min(1).max(100).optional(),
      offset: z.number().int().min(0).optional(),
    },
  },
  async ({ shop_name, limit, offset }) =>
    handle(() => client.get("/application/shops", { shop_name, limit, offset })),
);

server.registerTool(
  "get_shop",
  {
    title: "Get an Etsy shop",
    description: "Fetch details for a single Etsy shop by its shop id.",
    inputSchema: { shop_id: z.union([z.string(), z.number()]) },
  },
  async ({ shop_id }) => handle(() => client.get(`/application/shops/${shop_id}`)),
);

server.registerTool(
  "get_shop_sections",
  {
    title: "Get shop sections",
    description: "List the listing sections (categories) a shop has defined.",
    inputSchema: { shop_id: z.union([z.string(), z.number()]) },
  },
  async ({ shop_id }) => handle(() => client.get(`/application/shops/${shop_id}/sections`)),
);

server.registerTool(
  "get_shop_reviews",
  {
    title: "Get shop reviews",
    description: "List reviews left for a shop's listings.",
    inputSchema: {
      shop_id: z.union([z.string(), z.number()]),
      limit: z.number().int().min(1).max(100).optional(),
      offset: z.number().int().min(0).optional(),
    },
  },
  async ({ shop_id, limit, offset }) =>
    handle(() => client.get(`/application/shops/${shop_id}/reviews`, { limit, offset })),
);

// ---------------------------------------------------------------------------
// Listings
// ---------------------------------------------------------------------------

server.registerTool(
  "search_active_listings",
  {
    title: "Search active Etsy listings",
    description:
      "Search all active listings across Etsy (marketplace-wide) with an optional keyword and filters.",
    inputSchema: {
      keywords: z.string().optional(),
      shop_id: z.union([z.string(), z.number()]).optional(),
      taxonomy_id: z.number().int().optional(),
      min_price: z.number().optional(),
      max_price: z.number().optional(),
      sort_on: z.enum(["created", "price", "updated", "score"]).optional(),
      sort_order: z.enum(["asc", "desc", "ascending", "descending", "up", "down"]).optional(),
      limit: z.number().int().min(1).max(100).optional(),
      offset: z.number().int().min(0).optional(),
    },
  },
  async (params) => handle(() => client.get("/application/listings/active", params)),
);

server.registerTool(
  "get_listing",
  {
    title: "Get an Etsy listing",
    description: "Fetch a single listing by id, optionally including images/inventory/shop/user.",
    inputSchema: {
      listing_id: z.union([z.string(), z.number()]),
      includes: z
        .array(z.enum(["Shipping", "Images", "Shop", "User", "Translations", "Inventory", "Videos"]))
        .optional()
        .describe("Associated resources to embed in the response"),
    },
  },
  async ({ listing_id, includes }) =>
    handle(() => client.get(`/application/listings/${listing_id}`, { includes })),
);

server.registerTool(
  "get_listings_by_shop",
  {
    title: "Get a shop's active listings",
    description: "List a shop's currently active listings.",
    inputSchema: {
      shop_id: z.union([z.string(), z.number()]),
      limit: z.number().int().min(1).max(100).optional(),
      offset: z.number().int().min(0).optional(),
      sort_on: z.enum(["created", "price", "updated"]).optional(),
      sort_order: z.enum(["asc", "desc"]).optional(),
    },
  },
  async ({ shop_id, ...query }) =>
    handle(() => client.get(`/application/shops/${shop_id}/listings/active`, query)),
);

server.registerTool(
  "get_listing_images",
  {
    title: "Get listing images",
    description: "List all images attached to a listing.",
    inputSchema: { listing_id: z.union([z.string(), z.number()]) },
  },
  async ({ listing_id }) =>
    handle(() => client.get(`/application/listings/${listing_id}/images`)),
);

server.registerTool(
  "get_listing_inventory",
  {
    title: "Get listing inventory",
    description: "Get the products, SKUs, price/quantity variations for a listing.",
    inputSchema: { listing_id: z.union([z.string(), z.number()]) },
  },
  async ({ listing_id }) =>
    handle(() => client.get(`/application/listings/${listing_id}/inventory`)),
);

server.registerTool(
  "create_draft_listing",
  {
    title: "Create a draft listing (requires OAuth)",
    description:
      "Create a new draft physical listing in a shop. Requires an OAuth access token with the listings_w scope.",
    inputSchema: {
      shop_id: z.union([z.string(), z.number()]),
      title: z.string(),
      description: z.string(),
      price: z.number().positive(),
      quantity: z.number().int().positive(),
      who_made: z.enum(["i_did", "someone_else", "collective"]),
      when_made: z.string().describe('Etsy "when made" enum value, e.g. "made_to_order", "2020_2025"'),
      taxonomy_id: z.number().int(),
      shipping_profile_id: z.number().int().optional(),
      materials: z.array(z.string()).optional(),
      tags: z.array(z.string()).max(13).optional(),
      is_supply: z.boolean().optional(),
    },
  },
  async ({ shop_id, ...body }) =>
    handle(() => client.post(`/application/shops/${shop_id}/listings`, body)),
);

server.registerTool(
  "update_listing",
  {
    title: "Update a listing (requires OAuth)",
    description: "Update fields on an existing listing owned by the authenticated shop.",
    inputSchema: {
      shop_id: z.union([z.string(), z.number()]),
      listing_id: z.union([z.string(), z.number()]),
      title: z.string().optional(),
      description: z.string().optional(),
      price: z.number().positive().optional(),
      quantity: z.number().int().positive().optional(),
      tags: z.array(z.string()).max(13).optional(),
      state: z.enum(["active", "inactive", "draft"]).optional(),
    },
  },
  async ({ shop_id, listing_id, ...body }) =>
    handle(() => client.patch(`/application/shops/${shop_id}/listings/${listing_id}`, body)),
);

server.registerTool(
  "delete_listing",
  {
    title: "Delete a listing (requires OAuth)",
    description: "Permanently delete a listing owned by the authenticated shop.",
    inputSchema: { listing_id: z.union([z.string(), z.number()]) },
  },
  async ({ listing_id }) => handle(() => client.delete(`/application/listings/${listing_id}`)),
);

// ---------------------------------------------------------------------------
// Receipts / orders (requires OAuth)
// ---------------------------------------------------------------------------

server.registerTool(
  "get_shop_receipts",
  {
    title: "Get shop receipts / orders (requires OAuth)",
    description: "List order receipts for a shop the authenticated user owns.",
    inputSchema: {
      shop_id: z.union([z.string(), z.number()]),
      limit: z.number().int().min(1).max(100).optional(),
      offset: z.number().int().min(0).optional(),
      was_paid: z.boolean().optional(),
      was_shipped: z.boolean().optional(),
      min_created: z.number().int().optional().describe("Unix timestamp"),
      max_created: z.number().int().optional().describe("Unix timestamp"),
    },
  },
  async ({ shop_id, ...query }) =>
    handle(() => client.get(`/application/shops/${shop_id}/receipts`, query, true)),
);

server.registerTool(
  "get_shop_receipt",
  {
    title: "Get a single shop receipt (requires OAuth)",
    description: "Fetch one order receipt by id.",
    inputSchema: {
      shop_id: z.union([z.string(), z.number()]),
      receipt_id: z.union([z.string(), z.number()]),
    },
  },
  async ({ shop_id, receipt_id }) =>
    handle(() => client.get(`/application/shops/${shop_id}/receipts/${receipt_id}`, {}, true)),
);

server.registerTool(
  "create_receipt_shipment",
  {
    title: "Mark a receipt as shipped (requires OAuth)",
    description: "Submit tracking info and mark an order receipt as shipped.",
    inputSchema: {
      shop_id: z.union([z.string(), z.number()]),
      receipt_id: z.union([z.string(), z.number()]),
      tracking_code: z.string().optional(),
      carrier_name: z.string().optional(),
      send_bcc: z.boolean().optional(),
      note_to_buyer: z.string().optional(),
    },
  },
  async ({ shop_id, receipt_id, ...body }) =>
    handle(() =>
      client.post(`/application/shops/${shop_id}/receipts/${receipt_id}/tracking`, body),
    ),
);

// ---------------------------------------------------------------------------
// Taxonomy / users / misc
// ---------------------------------------------------------------------------

server.registerTool(
  "get_seller_taxonomy",
  {
    title: "Get seller taxonomy nodes",
    description:
      "Fetch the full Etsy seller taxonomy tree (categories used for taxonomy_id when creating listings).",
    inputSchema: {},
  },
  async () => handle(() => client.get("/application/seller-taxonomy/nodes")),
);

server.registerTool(
  "get_taxonomy_properties",
  {
    title: "Get properties for a taxonomy node",
    description: "List the item properties (e.g. color, size) available for a taxonomy category.",
    inputSchema: { taxonomy_id: z.number().int() },
  },
  async ({ taxonomy_id }) =>
    handle(() => client.get(`/application/seller-taxonomy/nodes/${taxonomy_id}/properties`)),
);

server.registerTool(
  "get_authenticated_user",
  {
    title: "Get the authenticated user (requires OAuth)",
    description: "Fetch the Etsy user profile associated with the configured OAuth access token.",
    inputSchema: {},
  },
  async () => {
    const userId = client.getAuthenticatedUserId();
    if (!userId) {
      return errorResult(
        new Error("No OAuth access token configured (ETSY_ACCESS_TOKEN). See README for setup."),
      );
    }
    return handle(() => client.get(`/application/users/${userId}`, {}, true));
  },
);

// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("etsy-mcp-server running on stdio");
}

main().catch((err) => {
  console.error("Fatal error starting etsy-mcp-server:", err);
  process.exit(1);
});
