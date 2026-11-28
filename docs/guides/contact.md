# Contact form

Reserva has a contact form for questions, privacy requests, business enquiries and bug reports. The form
posts to a public endpoint of the auth service, so you can send a message from your own application too.
Messages are stored and handled by the Reserva team; there is no e-mail address to write to.

## Send a message

`POST /auth/contact` needs no token. If you send a valid `Authorization: Bearer` header, the message is
linked to that user. Without it the message is sent as a guest.

```bash
curl -X POST "https://reserva.bojanlab.com/auth/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo User",
    "email": "<your e-mail address>",
    "category": "GENERAL",
    "message": "Hello, I would like to know how to connect my business to Reserva.",
    "honeypot": ""
  }'
```

A successful call returns `204 No Content` with no body.

| Field | Required | Rules |
| --- | --- | --- |
| `name` | yes | At most 100 characters. |
| `email` | yes | A valid e-mail address where the sender can be reached. |
| `category` | yes | One of `GENERAL`, `PRIVACY`, `BUSINESS`, `BUG`. |
| `message` | yes | 10 to 5000 characters. |
| `honeypot` | no | Spam trap. Leave it empty or omit it. |

!!! warning "Keep `honeypot` empty"
    The form on the Reserva site has a hidden field that real users never fill in. If it contains a
    value, the request is treated as spam: it still returns `204`, but the message is not stored.

## Errors

| Status | Error code | Meaning |
| --- | --- | --- |
| `400` | | The body is invalid. The response has a `message` that lists the failing fields and reasons. |
| `429` | `error.contact_message.rate_limit_exceeded` | Too many messages from the same IP address. Try again later. |
