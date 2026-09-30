# Issue 001: Swagger UI returns HTTP 500

**Date:** 2026-04-01
**App:** job_portal
**Tool:** swfaw (AuthorizationWebFilter template)
**Severity:** High

## Symptom
`GET /swagger-ui.html` returns HTTP 500 with empty body. The redirect to `/webjars/swagger-ui/index.html` never completes.

## Root Cause
`AuthorizationWebFilter.filter()` called `handlerMapping.getHandler(exchange).cast(HandlerMethod.class)` on every request. Swagger's redirect handler is not a `HandlerMethod` — the `.cast()` threw `ClassCastException`, surfacing as 500.

## Fix
Added path-based early return at the top of the filter method. Non-API paths (`/swagger-ui/**`, `/webjars/**`, `/setup/**`, `/api/auth/**`, etc.) now skip the filter entirely.

**File changed:** `swfaw/templates/authorization_service_templates.py` — `AUTHORIZATION_WEB_FILTER` template

**Before:**
```java
return handlerMapping.getHandler(exchange)
    .cast(HandlerMethod.class)
    .flatMap(handlerMethod -> { ... })
```

**After:**
```java
String path = exchange.getRequest().getURI().getPath();
if (!path.startsWith("/api/") || path.startsWith("/api/auth/")) {
    return chain.filter(exchange);
}
return handlerMapping.getHandler(exchange)
    .flatMap(handler -> {
        if (!(handler instanceof HandlerMethod)) {
            return chain.filter(exchange);
        }
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        ...
    })
```

## Verification
- `GET /swagger-ui.html` → 302 → `/webjars/swagger-ui/index.html` → 200
- `GET /v3/api-docs` → 200 (was already working)
- All 25 API endpoints still return 401 (auth working correctly)
