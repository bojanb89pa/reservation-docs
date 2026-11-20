# Changelog

Entries are newest first. A breaking change is marked **Breaking** at the top of its entry. During the
preview there is no deprecation period.

## 0.4.0 — 2026-11-20

Reserva can be connected to AI assistants through an MCP server, and reservation responses show where a
reservation came from. There are no breaking changes.

- New: `POST /api/mcp` is the MCP server endpoint (stateless Streamable HTTP). It needs a token issued for
  the MCP resource; without a valid token it returns `401` with a `WWW-Authenticate` header that points to
  the resource metadata. Tools: search, business details, free slots, create, list, get and cancel
  reservation. See [Connect Reserva to AI assistants](guides/mcp.md).
- New: `GET /api/.well-known/oauth-protected-resource` and
  `GET /api/.well-known/oauth-protected-resource/mcp` return the OAuth Protected Resource Metadata
  (RFC 9728) of the MCP server: resource, authorization servers and the scopes `reservations:read` and
  `reservations:write`.
- Changed: reservation responses have two new fields, `origin` (`RESERVA_APP`, `CLIENT_APPLICATION` or
  `AI_ASSISTANT`) and `originClient` (client name, for `AI_ASSISTANT` only, otherwise `null`). They appear in
  `GET /api/reservations`, `POST /api/resources/{resourceId}/reservations`,
  `GET /api/resources/{resourceId}/reservations/{id}` and
  `POST /api/resources/{resourceId}/reservations/{id}/cancel`. Requests are unchanged. Treat an unknown
  `origin` value as `RESERVA_APP`.
- Tokens for the MCP server are not accepted by the REST endpoints, and REST or partner tokens are not
  accepted by `POST /api/mcp`.

## 0.3.0 — 2026-11-08

Partners can cancel the reservations they made. There are no breaking changes.

- New: `POST /api/client-applications/reservations/{id}/cancel` cancels a reservation that your application
  made for the token's user. It needs the new scope `reservation:cancel:own` and returns the updated
  reservation. Errors: `403` without the scope, `404` for an unknown or foreign reservation, `422` when the
  business cancellation policy does not allow it.
- New scope `reservation:cancel:own` for `POST /auth/oauth2/token`. It is granted only when it is in the
  application's allowed scopes, so existing applications do not get it automatically.
- The booking widget has no cancel button yet.

## 0.2.0 — 2026-11-06

Documentation of four read-only endpoints that were already available on staging. There are no breaking
changes.

- Search suggestions: `GET /api/v1/search/suggestions` returns autocomplete suggestions (places,
  categories, businesses) for a typed query.
- Lookup by ID: `GET /api/businesses/{id}` and `GET /api/business-categories/{id}` return one business or
  category, with the category name localized by `Accept-Language`.
- Reservations: `GET /api/resources/{resourceId}/reservations/{id}` returns one reservation and needs an
  access token.

## 0.1.0 — 2026-11-04

First public preview.

- Resource API: search businesses, read business details, locations, services and resources, list free
  slots, and create, list and cancel reservations of a signed-in Reserva user.
- Partner reservations: `POST /api/client-applications/reservations`,
  `GET /api/client-applications/reservations` and `GET /api/client-applications/reservations/{id}`.
- Auth API: token endpoint with token exchange for partners (OIDC ID token or partner-signed JWT), JWKS
  and discovery documents.
- Booking widget: loader, light and dark themes, guest slot selection with `onSignInRequired`, and the
  mandatory "by Reserva" mark.
