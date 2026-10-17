# Maya Node frontend recovery and deployment

## Keep the website separate from the protected Worker

The customer-facing React/Vite website lives in `frontend/`. It contains the Home, About, Services, Pricing, Contact, and Consultation routes.

The Cloudflare Worker under `deploy/cloudflare/` is a separate protected backend/staging component. Its root URL can return `401 Unauthorized` by design because controller-token authentication is required. That URL is not the customer website.

## Build verification and recovery artifact

The `Frontend build and lint` GitHub Actions workflow runs the frontend lint and production build when frontend files change. It now also uploads the built static site as the `maya-node-frontend-dist` workflow artifact. The artifact is retained for 14 days, provided the build succeeds.

In GitHub, open **Actions → Frontend build and lint → a successful run → Artifacts → maya-node-frontend-dist** to retrieve the generated `dist/` site files.

## Cloudflare Pages settings for the customer website

If deploying the customer-facing site as a Cloudflare Pages project connected to this repository, use:

- **Production branch:** `main`
- **Root directory (if the field is shown):** `frontend` (relative to the repository root; no leading slash)
- **Build command:** `npm run build`
- **Build output directory:** `dist` (relative to `frontend/`)

These settings apply to the frontend Pages project, not the existing Worker deployment.

## Existing Worker deployment failure

The recorded Worker build failed while cloning because Cloudflare reported that configured root directory `/deploy/cloudflare` was not found. The directory exists in the GitHub repository. Verify the Worker build's root-directory setting is relative to the repository root and matches `deploy/cloudflare`. If the UI does not require a root directory, another valid approach is to leave it at the repository root and configure the Wrangler command to use `deploy/cloudflare/wrangler.jsonc`; do not apply both approaches without checking the build configuration.

## Safety and scope

- Do not remove controller-token authentication to make the Worker root URL look public.
- Keep `SEND_ENABLED=false` while restoring and testing.
- A successful frontend build proves the site can be built; it does not prove a live deployment, customer integrations, or email delivery. Verify the public URL after deploying.
