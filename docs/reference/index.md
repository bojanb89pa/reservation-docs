# API reference

The reference is generated from the OpenAPI documents that staging publishes. It is never edited by hand:
descriptions, parameters and examples come from the Reserva source code.

| API | Reference | OpenAPI document |
| --- | --- | --- |
| Resource API (`/api`) | [Open the Resource API reference](resource.html) | [resource.json](../openapi/resource.json) |
| Auth API (`/auth`) | [Open the Auth API reference](auth.html) | [auth.json](../openapi/auth.json) |

The documents are refreshed automatically after every staging deploy, so the reference always matches what
runs on staging. "Try it" is turned off during the preview. Use the `curl` examples in the guides instead.

You can load the OpenAPI documents into your own tools (Postman, Insomnia, code generators). The `servers`
field is removed from them, because the base URL depends on the environment. See
[Getting started](../getting-started.md#environment) for the URLs.
