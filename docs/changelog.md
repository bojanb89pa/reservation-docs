# Changelog

Entries are newest first. A breaking change is marked **Breaking** at the top of its entry. During the
preview there is no deprecation period.

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
