# Issue 014: DELETE returns 404 for records that exist — CRUD otherwise works

**Date:** 2026-04-03
**App:** job_portal
**Tool:** swfaw (service_templates.py, auth_repository_templates.py)
**Severity:** Critical

## Symptom
`DELETE /api/education_levels/{id}` returns 404 "Entity not found" even though GET, PUT, and list all work for the same record.

## Investigation
- Create ✅, GET by ID ✅, Update ✅, List ✅, Delete ❌
- The delete method uses `SecurityContextHolder.getCurrentUser(exchange, ...).flatMap(user -> repository.findById(id)...)`
- The same pattern works for update
- R2DBC SQL logging shows the correct `SELECT ... WHERE education_level_id = ?` query for GET/PUT but no SELECT appears in logs for DELETE
- Added `@Query` annotation to `deleteByTableNameAndRecordId` in RecordOwnerRepository — didn't help
- Added exchange-based fallback to `SecurityContextHolder.getCurrentUser` — didn't help

## Possible causes (not yet confirmed)
1. The `Mono<Void>` return type causes the reactive chain to behave differently
2. The `SecurityContextHolder.getCurrentUser()` returns empty for DELETE (reactive context not propagated), and the fallback via exchange header also fails
3. The `activityTrackingService.logDelete()` call inside the chain might be failing and swallowing the error
4. R2DBC connection pool issue — the fallback's `authUserRepository.findByUsername()` and the subsequent `repository.findById()` might conflict

## Analysis (2026-04-10)

### Finding 1: Inconsistent SecurityContextHolder call

The `create` and `update` methods use the no-args version:
```java
SecurityContextHolder.getCurrentUser()
```
The `delete` method uses the 3-arg overload with exchange fallback:
```java
SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
```
The 3-arg version was added as an attempted fix but may be introducing the problem. The no-args version works fine for create/update — if the reactive security context propagates correctly for those, the fallback path in delete may be hitting an error and swallowing the chain.

### Finding 2: Reactive chain fragility with Mono<Void> and .then()

The delete chain:
```java
return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
    .flatMap(user -> 
        repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException(...)))
            .flatMap(entity -> activityTrackingService.logDelete(...)
                .then(repository.deleteById(id)))
            .then(recordOwnerRepository.deleteByTableNameAndRecordId(...))
    );
```
- `activityTrackingService.logDelete()` returns `Mono<Void>`. If it errors silently or the entity serialization inside it fails, the whole chain dies.
- Compare with `update`, which uses `.thenReturn(saved)` to keep the value flowing — more resilient.
- The triple `.then()` chaining discards values at each step, making it harder to diagnose where the chain breaks.

## Next steps
1. Test delete with no-args `SecurityContextHolder.getCurrentUser()` (same as create/update) — if it works, the 3-arg fallback is the culprit
2. Test delete without `activityTrackingService.logDelete()` — isolate whether activity tracking breaks the chain
3. Fix will be in swfaw service template — delete method template needs to match the pattern that works for create/update
