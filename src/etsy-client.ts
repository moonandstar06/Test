/**
 * Thin client for the Etsy Open API v3.
 *
 * Auth model:
 * - Every request needs the app's API key (x-api-key header).
 * - Endpoints that touch private data (shop management, receipts, creating
 *   listings, etc.) additionally need an OAuth 2.0 bearer token scoped to
 *   the relevant permissions. If a refresh token is configured, expired
 *   access tokens are refreshed automatically and the caller is notified
 *   via `onTokenRefresh` so it can persist the new pair.
 */

export interface EtsyClientConfig {
  apiKey: string;
  accessToken?: string;
  refreshToken?: string;
  baseUrl?: string;
  onTokenRefresh?: (tokens: { accessToken: string; refreshToken: string }) => void;
}

export class EtsyApiError extends Error {
  constructor(
    public status: number,
    public body: unknown,
    message: string,
  ) {
    super(message);
    this.name = "EtsyApiError";
  }
}

const DEFAULT_BASE_URL = "https://openapi.etsy.com/v3";
const TOKEN_URL = "https://api.etsy.com/v3/public/oauth/token";

export class EtsyClient {
  private apiKey: string;
  private accessToken?: string;
  private refreshToken?: string;
  private baseUrl: string;
  private onTokenRefresh?: EtsyClientConfig["onTokenRefresh"];
  private refreshingPromise: Promise<void> | null = null;

  constructor(config: EtsyClientConfig) {
    if (!config.apiKey) {
      throw new Error("EtsyClient requires an apiKey (ETSY_API_KEY)");
    }
    this.apiKey = config.apiKey;
    this.accessToken = config.accessToken;
    this.refreshToken = config.refreshToken;
    this.baseUrl = config.baseUrl ?? DEFAULT_BASE_URL;
    this.onTokenRefresh = config.onTokenRefresh;
  }

  get hasOAuth(): boolean {
    return Boolean(this.accessToken);
  }

  /** Etsy access tokens embed the numeric user/shop id before the first '.': "12345678.abcdef..." */
  getAuthenticatedUserId(): string | undefined {
    if (!this.accessToken) return undefined;
    return this.accessToken.split(".")[0];
  }

  private async refreshAccessToken(): Promise<void> {
    if (!this.refreshToken) {
      throw new Error(
        "Access token expired/missing and no ETSY_REFRESH_TOKEN was configured to renew it.",
      );
    }
    if (this.refreshingPromise) {
      return this.refreshingPromise;
    }
    this.refreshingPromise = (async () => {
      const res = await fetch(TOKEN_URL, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          grant_type: "refresh_token",
          client_id: this.apiKey,
          refresh_token: this.refreshToken!,
        }),
      });
      if (!res.ok) {
        const body = await res.text();
        throw new EtsyApiError(res.status, body, `Failed to refresh Etsy OAuth token: ${body}`);
      }
      const data = (await res.json()) as { access_token: string; refresh_token: string };
      this.accessToken = data.access_token;
      this.refreshToken = data.refresh_token;
      this.onTokenRefresh?.({ accessToken: data.access_token, refreshToken: data.refresh_token });
    })();
    try {
      await this.refreshingPromise;
    } finally {
      this.refreshingPromise = null;
    }
  }

  async request<T = unknown>(
    method: string,
    path: string,
    options: { query?: Record<string, unknown>; body?: unknown; requiresAuth?: boolean } = {},
  ): Promise<T> {
    const { query, body, requiresAuth = false } = options;

    if (requiresAuth && !this.accessToken) {
      throw new Error(
        `This operation requires an OAuth access token (ETSY_ACCESS_TOKEN). See README for the OAuth setup flow.`,
      );
    }

    const url = new URL(this.baseUrl + path);
    if (query) {
      for (const [key, value] of Object.entries(query)) {
        if (value === undefined || value === null) continue;
        if (Array.isArray(value)) {
          url.searchParams.set(key, value.join(","));
        } else {
          url.searchParams.set(key, String(value));
        }
      }
    }

    const doFetch = async (): Promise<Response> => {
      const headers: Record<string, string> = { "x-api-key": this.apiKey };
      if (this.accessToken) headers["Authorization"] = `Bearer ${this.accessToken}`;
      if (body !== undefined) headers["Content-Type"] = "application/json";
      return fetch(url, {
        method,
        headers,
        body: body !== undefined ? JSON.stringify(body) : undefined,
      });
    };

    let res = await doFetch();

    if (res.status === 401 && this.refreshToken) {
      await this.refreshAccessToken();
      res = await doFetch();
    }

    if (!res.ok) {
      let parsedBody: unknown;
      const text = await res.text();
      try {
        parsedBody = JSON.parse(text);
      } catch {
        parsedBody = text;
      }
      const message =
        typeof parsedBody === "object" && parsedBody && "error" in (parsedBody as any)
          ? String((parsedBody as any).error)
          : `Etsy API request failed with status ${res.status}`;
      throw new EtsyApiError(res.status, parsedBody, message);
    }

    if (res.status === 204) {
      return undefined as T;
    }
    return (await res.json()) as T;
  }

  get<T = unknown>(path: string, query?: Record<string, unknown>, requiresAuth = false) {
    return this.request<T>("GET", path, { query, requiresAuth });
  }

  post<T = unknown>(path: string, body?: unknown, query?: Record<string, unknown>) {
    return this.request<T>("POST", path, { body, query, requiresAuth: true });
  }

  put<T = unknown>(path: string, body?: unknown, query?: Record<string, unknown>) {
    return this.request<T>("PUT", path, { body, query, requiresAuth: true });
  }

  patch<T = unknown>(path: string, body?: unknown, query?: Record<string, unknown>) {
    return this.request<T>("PATCH", path, { body, query, requiresAuth: true });
  }

  delete<T = unknown>(path: string, query?: Record<string, unknown>) {
    return this.request<T>("DELETE", path, { query, requiresAuth: true });
  }
}
