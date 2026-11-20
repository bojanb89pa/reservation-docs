# Connect Reserva to AI assistants (MCP)

Reserva runs a [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server. An AI assistant that
supports remote MCP connectors, for example Claude, can use it to find a business, look up free slots, and
book, list and cancel reservations for the signed-in Reserva user, all from a conversation.

!!! warning "Preview, staging only"
    The MCP server is available on staging only (`https://reserva.bojanlab.com`), with demo data. It may
    change without notice.

## 1. Endpoint

| Item | Value |
| --- | --- |
| MCP endpoint | `https://reserva.bojanlab.com/api/mcp` |
| Transport | Streamable HTTP, stateless (no session) |
| Authorization | OAuth 2.0 bearer token issued by the [Auth API](../authentication.md) |

The endpoint is `POST /api/mcp`. Normally you do not call it by hand: the assistant speaks the protocol.

## 2. Add the connector

1. In your assistant, add a custom (remote) connector and enter `https://reserva.bojanlab.com/api/mcp` as
   the server URL.
2. The assistant discovers how to sign in (see below) and opens the Reserva sign-in page.
3. Sign in as a Reserva user and approve the requested scopes.
4. Ask the assistant, for example, "Find a hairdresser near me and book the first free slot tomorrow."

## 3. How sign-in is discovered

A request without a token, or with an invalid one, gets `401` and a `WWW-Authenticate` header:

```bash
curl -i -X POST https://reserva.bojanlab.com/api/mcp
```

```http
HTTP/1.1 401
WWW-Authenticate: Bearer resource_metadata="https://reserva.bojanlab.com/api/.well-known/oauth-protected-resource", scope="reservations:read reservations:write"
```

The `resource_metadata` URL points to the Protected Resource Metadata document (RFC 9728). It is public:

```bash
curl https://reserva.bojanlab.com/api/.well-known/oauth-protected-resource
```

```json
{
  "resource": "https://reserva.bojanlab.com/api/mcp",
  "authorization_servers": ["https://reserva.bojanlab.com/auth"],
  "scopes_supported": ["reservations:read", "reservations:write"],
  "bearer_methods_supported": ["header"]
}
```

The same document is also served at `GET /api/.well-known/oauth-protected-resource/mcp`. The
`authorization_servers` value is the issuer of the [Auth API](../authentication.md); the assistant reads
its discovery document to find the authorization and token endpoints. Always read the exact values from
the endpoint.

## 4. Tokens and audience

- `POST /api/mcp` accepts only a token issued for the MCP resource (the `aud` claim equals the `resource`
  value above).
- That token is **not** accepted by the REST endpoints, and a REST or partner token is **not** accepted by
  `POST /api/mcp`.
- When a tool needs a scope the token does not have, the call is rejected with `insufficient_scope` and the
  scope that is required.

## 5. Tools

| Tool | What it does | Scope |
| --- | --- | --- |
| `search_businesses` | Searches businesses. | any valid token |
| `get_business` | Returns a business with its locations, services and resources. | any valid token |
| `get_free_slots` | Free slots of a resource for one day or a range of up to 7 days, in the location's local time. | any valid token |
| `create_reservation` | Books a slot. | `reservations:write` |
| `list_my_reservations` | Lists your reservations (upcoming by default). | `reservations:read` |
| `get_reservation` | Returns one reservation. | `reservations:read` |
| `cancel_reservation` | Cancels a reservation, subject to the business cancellation policy. | `reservations:write` |

Notes:

- `create_reservation` and `cancel_reservation` are marked as destructive, so assistants ask you to
  confirm. Their result repeats the business, service, time (local) and price.
- `create_reservation` accepts an optional `client_request_id`. The same user and the same key within 24
  hours return the same reservation instead of a new one.
- `create_reservation` is rate limited per user. When the limit is reached the tool returns an error result.
- Business errors (slot taken, cancellation not allowed, unknown ID) are returned as tool error results with
  a message the assistant can show to you. They are not HTTP errors.

## 6. Reservation origin

A reservation made through the MCP server belongs to the user in the token. The business does not approve
this channel. Every reservation response now carries two fields that tell where it came from:

```bash
curl -H "Authorization: Bearer $TOKEN" https://reserva.bojanlab.com/api/reservations
```

```json
[
  {
    "id": "...",
    "status": "CONFIRMED",
    "origin": "AI_ASSISTANT",
    "originClient": "Claude"
  }
]
```

| Field | Values |
| --- | --- |
| `origin` | `RESERVA_APP`, `CLIENT_APPLICATION` (partner reservations) or `AI_ASSISTANT`. Always present. Treat an unknown value as `RESERVA_APP`; the list can grow. |
| `originClient` | The client name, for example `Claude`. Set only when `origin` is `AI_ASSISTANT`, otherwise `null`. It comes from outside: show it as plain text, never as HTML. |

The fields are in the responses of `GET /api/reservations`, `POST /api/resources/{resourceId}/reservations`,
`GET /api/resources/{resourceId}/reservations/{id}` and
`POST /api/resources/{resourceId}/reservations/{id}/cancel`. Request bodies are unchanged.

## 7. Limits of the preview

- Staging only, demo data, no production URL.
- The tools cover the booking flow only; there are no tools for business management.
- Text from the database (business names and descriptions) appears only in tool results, shortened.
