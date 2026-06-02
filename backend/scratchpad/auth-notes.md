# Backend Auth Notes

Authentication and authorization should be treated as separate steps.

Authentication answers: is this request from a real logged-in user?

Authorization answers: is this logged-in user allowed to access or change this
specific resource?

If all backend APIs are private, middleware is a reasonable place to verify the
bearer token on every request:

```text
Authorization: Bearer <access_token>
```

The middleware can verify the token signature, expiry, and issuer, then attach
the authenticated identity to the request:

```py
request.state.user = {
    "id": token_payload["sub"],
    "email": token_payload["email"],
}
```

Use dependencies or service-layer checks for route-specific authorization. In
FastAPI, a "guard" is usually just a dependency.

Important rule: never trust `user_id`, `organization_id`, `role`, or
`permissions` from the client body or URL as proof that the caller is allowed to
use that data. The token tells you who the caller is; the backend must then
decide whether that caller can access the requested target.

Example:

```text
GET /api/v1/users/42
Authorization: Bearer token_for_user_7
```

The backend must not return user `42` just because `42` is in the URL. It should
check whether token user `7` is allowed to access user `42`. Usually this should
be rejected unless the requester has an admin/owner role or another explicit
permission.

Prefer self-scoped routes where possible:

```text
GET /api/v1/me
PATCH /api/v1/me
```

For organization/workspace routes, check membership and role:

```py
if not user_belongs_to_org(current_user.id, organization_id):
    raise HTTPException(status_code=403, detail="Forbidden")

if not has_permission(current_user.id, organization_id, "roles.assign"):
    raise HTTPException(status_code=403, detail="Forbidden")
```

Practical split:

- Middleware: verify token and attach current identity.
- Dependency: expose current user to routes, or declare route-level guards.
- Service layer: enforce ownership, organization membership, and permissions
  close to the business action.
