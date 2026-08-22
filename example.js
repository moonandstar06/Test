import { EtsyClient } from "./src/etsyClient.js";

const apiKey = process.env.ETSY_API_KEY;
const accessToken = process.env.ETSY_ACCESS_TOKEN; // optional, needed for user-scoped endpoints

if (!apiKey) {
  console.error("Set ETSY_API_KEY in your environment before running this example.");
  process.exit(1);
}

const client = new EtsyClient({ apiKey, accessToken });

const pong = await client.ping();
console.log("Ping:", pong);

const shopName = process.argv[2];
if (shopName) {
  const shops = await client.findShops(shopName, { limit: 5 });
  console.log(`Shops matching "${shopName}":`, shops);
}
