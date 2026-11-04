# Reserva API

Reserva is an online booking platform for service businesses: barbers, beauty salons, clinics and similar.
This site documents the parts of Reserva that other applications can use:

- the **public REST API**: search businesses, read their locations, services and resources, check free
  slots, and create, list and cancel reservations;
- the **authorization server**: OAuth2 tokens, including token exchange for partner applications;
- the **booking widget**: an iframe that a partner embeds on its own website.

!!! warning "Preview"
    The API is in preview (version `0.x`). It may change without notice until general availability, and
    the only environment is staging. Breaking changes are marked at the top of each
    [changelog](changelog.md) entry.

## Where to start

| You want to | Read |
| --- | --- |
| Make your first calls against staging | [Getting started](getting-started.md) |
| Understand tokens, scopes and token exchange | [Authentication](authentication.md) |
| Let users of your website book with a Reserva business | [Partner integration](guides/partner-integration.md) and [Booking widget](guides/widget.md) |
| Look up an endpoint, parameter or response | [API reference](reference/index.md) |

## Two services

| Service | Path prefix | What it does |
| --- | --- | --- |
| Resource API | `/api` | Businesses, locations, services, resources, slots and reservations. |
| Auth API | `/auth` | OAuth2 authorization server: token endpoint, JWKS and discovery documents. |

The API reference shows only the public part of both services. Endpoints that are not listed there are
internal and may change or disappear at any time.
