# Getting started

## Environment

There is one environment, **staging**. It runs demo data and can be reset at any time.

| | URL |
| --- | --- |
| Resource API | `https://reserva.bojanlab.com/api` |
| Auth API | `https://reserva.bojanlab.com/auth` |
| Booking widget loader | `https://reserva.bojanlab.com/widget.js` |
| Demo partner website | <https://demo-business.bojanlab.com> |

All examples on this site use these URLs. When a production environment exists, it will be added to this
table and staging will stay available as a sandbox.

!!! note "Demo data only"
    Staging contains generated demo businesses and accounts. Do not use real personal data there, and do
    not rely on IDs staying the same after a reset.

## Read public data without a token

Searching businesses, reading their details and checking free slots does not need a token.

### 1. Find a business

`GET /api/v1/search` searches active businesses by name, category and service:

```bash
curl "https://reserva.bojanlab.com/api/v1/search?q=frizer&size=5"
```

```json
{
  "content": [
    {
      "businessId": "2b187165-3c35-4d6f-9edf-a9ec7dc73afe",
      "businessName": "Novosadski Frizer",
      "categoryId": "a0000000-0000-0000-0000-000000000001",
      "city": "Novi Sad",
      "similarityScore": 0.39,
      "imageUrl": null
    }
  ],
  "size": 5,
  "page": 0,
  "totalElements": 1,
  "totalPages": 1
}
```

Pagination is zero-based (`page`, `size`). Other ways to find businesses are
`GET /api/businesses/search` (filters), `GET /api/businesses/nearby` (coordinates) and
`GET /api/businesses/category/{categoryId}`. Categories come from `GET /api/business-categories`.

### 2. Read locations, services and resources

```bash
BUSINESS=<businessId>
curl "https://reserva.bojanlab.com/api/businesses/$BUSINESS/locations"
curl "https://reserva.bojanlab.com/api/businesses/$BUSINESS/services"
curl "https://reserva.bojanlab.com/api/businesses/$BUSINESS/resources"
```

- A **location** is a physical branch of the business (`GET /api/businesses/{businessId}/locations`).
- A **service** is what a customer books, with its duration rules (`GET /api/businesses/{businessId}/services`).
- A **resource** is who or what performs the service, for example an employee or a chair
  (`GET /api/businesses/{businessId}/resources`).

### 3. Check free slots

`GET /api/resources/{resourceId}/slots` returns fixed-length slots of a resource for one service in a date
range. Dates use `yyyy-MM-dd`:

```bash
curl "https://reserva.bojanlab.com/api/resources/<resourceId>/slots?serviceId=<serviceId>&from=2026-11-05&to=2026-11-05"
```

```json
[
  { "startTime": "2026-11-05T09:00:00", "endTime": "2026-11-05T09:30:00", "status": "AVAILABLE" },
  { "startTime": "2026-11-05T09:30:00", "endTime": "2026-11-05T10:00:00", "status": "CONFIRMED" }
]
```

Only `AVAILABLE` slots can be booked. `PENDING` and `CONFIRMED` slots are taken. Times are local times of
the business location, without a time zone offset.

## Book, list and cancel: you need a token

Creating, reading and cancelling reservations is done for a user, so these calls need an access token:

| Who books | Endpoints | How to get a token |
| --- | --- | --- |
| A signed-in Reserva user | `POST /api/resources/{resourceId}/reservations`, `GET /api/reservations`, `POST /api/resources/{resourceId}/reservations/{id}/cancel` | Authorization code flow |
| A partner application, for its own user | `POST /api/client-applications/reservations`, `GET /api/client-applications/reservations` | Token exchange |

Read [Authentication](authentication.md) next. If you are building a website for a business, the
[booking widget](guides/widget.md) does all of this for you.

## Getting access

Partner registration (a client application, its allowed origins and the business consent) is done by a
Reserva administrator during the preview. There is no self-service sign-up yet.
