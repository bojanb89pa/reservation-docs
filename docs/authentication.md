# Authentication

Reserva uses **OAuth2 with JWT access tokens**. The Auth API issues and signs tokens, and the Resource API
checks them on every request. Send the token as a bearer header:

```bash
curl -H "Authorization: Bearer <access_token>" "https://reserva.bojanlab.com/api/reservations"
```

Public read endpoints (search, business details, slots) work without a token. See the
[API reference](reference/index.md) for the security requirement of each endpoint.

## Endpoints

| Purpose | Endpoint |
| --- | --- |
| Token endpoint | `POST /auth/oauth2/token` |
| JSON Web Key Set (public signing keys) | `GET /auth/oauth2/jwks` |
| OpenID Connect discovery | `GET /auth/.well-known/openid-configuration` |
| OAuth2 authorization server metadata | `GET /auth/.well-known/oauth-authorization-server` |

Use the discovery documents instead of hard-coding the other URLs. If you verify Reserva tokens yourself,
take the keys from the JWKS and select the key by `kid`.

## Which flow to use

| Flow | `grant_type` | Who uses it |
| --- | --- | --- |
| Token exchange (RFC 8693) | `urn:ietf:params:oauth:grant-type:token-exchange` | Partner applications acting for their own signed-in users. This is the flow for integrations. |
| Authorization code | `authorization_code` | Reserva's own applications, where a Reserva user signs in on the Reserva login page. |
| Client credentials | `client_credentials` | Server-to-server calls of a registered confidential client. The token has no end user, so it cannot book. |

During the preview, every client (its ID, type, scopes and redirect URIs) is registered by a Reserva
administrator.

## Token exchange for partners

A partner application does not get passwords or Reserva accounts of its users. Instead it exchanges a proof
of its user's identity for a short-lived Reserva token:

1. Your user signs in on your site, with your own login.
2. Your page gets an identity token for that user. It is either an **OIDC ID token** from a trusted issuer
   such as Google (path 1), or a **JWT assertion signed by your backend** (path 2).
3. That token is exchanged for a Reserva access token at `POST /auth/oauth2/token`.
4. The Reserva token is used for partner reservation calls. Reservations are linked to your user's identity,
   not to a Reserva account.

The booking widget does steps 3 and 4 for you, inside its iframe. The details of both paths, including key
registration for path 2, are in the [partner integration guide](guides/partner-integration.md).

### Request

`application/x-www-form-urlencoded`. A partner client is a **public** client: it sends `client_id` and no
secret.

| Field | Value |
| --- | --- |
| `grant_type` | `urn:ietf:params:oauth:grant-type:token-exchange` |
| `client_id` | Your public client application ID. |
| `subject_token` | The ID token (path 1) or your signed assertion (path 2). |
| `subject_token_type` | `urn:ietf:params:oauth:token-type:id_token` (path 1) or `urn:ietf:params:oauth:token-type:jwt` (path 2). |
| `scope` | Optional, space-separated. Partner scopes are listed below. |

```bash
curl -X POST "https://reserva.bojanlab.com/auth/oauth2/token" \
  --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  --data-urlencode "client_id=<public client application id>" \
  --data-urlencode "subject_token=<id token or signed assertion>" \
  --data-urlencode "subject_token_type=urn:ietf:params:oauth:token-type:id_token" \
  --data-urlencode "scope=reservation:create reservation:read:own"
```

The response is a standard OAuth2 token response with `access_token`, `token_type` and `expires_in`.
The token lasts about 10 minutes and there is **no refresh token**. When it expires, exchange a fresh
identity token again.

### Errors

| `error` | Meaning |
| --- | --- |
| `invalid_client` | The client is unknown or has been disabled. |
| `invalid_grant` | The subject token was rejected: signature, issuer, audience, expiry, or a reused `jti`. |
| `invalid_scope` | A requested scope is not allowed for this client. |
| `invalid_request` | A required field is missing, or `subject_token_type` is wrong. |

## Scopes

| Scope | Allows |
| --- | --- |
| `reservation:create` | Creating a reservation for the token's end user: `POST /api/client-applications/reservations`. |
| `reservation:read:own` | Reading the reservations your application made for that user: `GET /api/client-applications/reservations` and `GET /api/client-applications/reservations/{id}`. |
| `openid`, `profile` | OpenID Connect scopes for Reserva's own sign-in. |
| `read`, `write` | General scopes of Reserva's own applications. |

A partner token never gives access to reservations made by other applications or on Reserva itself.

## Security rules for integrators

- Keep identity tokens and Reserva tokens out of logs and URLs.
- Never put a private key or a client secret in front-end code or in a repository.
- Request only the scopes you need.
- Treat `401` as "get a new token" and `403` as "this token is not allowed to do this".
