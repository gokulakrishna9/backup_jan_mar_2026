# Exception Handling Documentation

## Overview

Exception handling has been added to swfaw_v2 to provide proper validation error messages and structured error responses in Swagger UI.

## Components Added

### 1. Exception Templates (`templates/exception_templates.py`)

Contains Jinja2 templates for:
- **GlobalExceptionHandler** - Centralized exception handling with `@RestControllerAdvice`
- **ErrorResponse** - Standard error response structure
- **ValidationErrorResponse** - Validation error response with field-level details
- **EntityNotFoundException** - Custom exception for missing entities
- **AccessDeniedException** - Custom exception for authorization failures
- **DuplicateEntityException** - Custom exception for duplicate entities

### 2. Exception Generator (`generators/exception_generator.py`)

Generates Java exception handling classes from templates:
- `generate_global_exception_handler()` - Creates the global exception handler
- `generate_error_response()` - Creates the standard error response class
- `generate_validation_error_response()` - Creates validation error response class
- `generate_entity_not_found_exception()` - Creates EntityNotFoundException
- `generate_access_denied_exception()` - Creates AccessDeniedException
- `generate_duplicate_entity_exception()` - Creates DuplicateEntityException

### 3. Integration with main.py

Exception handling components are now generated automatically:
```python
# Generate Exception Classes
global_exception_handler_code = ExceptionGenerator.generate_global_exception_handler(package_name)
error_response_code = ExceptionGenerator.generate_error_response(package_name)
validation_error_response_code = ExceptionGenerator.generate_validation_error_response(package_name)
entity_not_found_exception_code = ExceptionGenerator.generate_entity_not_found_exception(package_name)
access_denied_exception_code = ExceptionGenerator.generate_access_denied_exception(package_name)
duplicate_entity_exception_code = ExceptionGenerator.generate_duplicate_entity_exception(package_name)
```

### 4. Updated Service Templates

Services now use proper exception classes instead of generic `RuntimeException`:
- `AccessDeniedException` for authorization failures
- `EntityNotFoundException` for missing entities
- Proper error messages with entity type and operation context

## Exception Handlers

### GlobalExceptionHandler

Handles the following exceptions:

1. **WebExchangeBindException** (400 Bad Request)
   - Triggered by `@Valid` annotation failures
   - Returns `ValidationErrorResponse` with field-level errors
   - Error code: `VALIDATION_ERROR`

2. **EntityNotFoundException** (404 Not Found)
   - Triggered when entity is not found by ID
   - Returns `ErrorResponse` with entity details
   - Error code: `ENTITY_NOT_FOUND`

3. **AccessDeniedException** (403 Forbidden)
   - Triggered when user lacks required permissions
   - Returns `ErrorResponse` with operation and resource details
   - Error code: `ACCESS_DENIED`

4. **DuplicateEntityException** (409 Conflict)
   - Triggered when attempting to create duplicate entity
   - Returns `ErrorResponse` with field and value details
   - Error code: `DUPLICATE_ENTITY`

5. **IllegalArgumentException** (400 Bad Request)
   - Triggered for invalid arguments
   - Returns `ErrorResponse`
   - Error code: `INVALID_ARGUMENT`

6. **RuntimeException** (500 Internal Server Error)
   - Catches all other runtime exceptions
   - Returns `ErrorResponse`
   - Error code: `RUNTIME_ERROR`

7. **Exception** (500 Internal Server Error)
   - Catches all other exceptions
   - Returns generic error message
   - Error code: `INTERNAL_ERROR`

## Error Response Structures

### Standard Error Response

```json
{
  "timestamp": "2026-03-10T14:30:00",
  "status": 404,
  "error": "Not Found",
  "message": "Entity with id 123 not found",
  "path": "/api/entities/123",
  "errorCode": "ENTITY_NOT_FOUND"
}
```

### Validation Error Response

```json
{
  "timestamp": "2026-03-10T14:30:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Validation failed for the request",
  "path": "/api/entities",
  "errorCode": "VALIDATION_ERROR",
  "fieldErrors": {
    "email": "email cannot be null",
    "name": "name cannot be null",
    "age": "age must be greater than 0"
  }
}
```

## Swagger Integration

All error responses are documented with Swagger annotations:
- `@Schema` descriptions on all fields
- Example values for documentation
- Proper HTTP status codes
- Field-level error details for validation failures

## Usage in Services

Services now throw proper exceptions:

```java
// Entity not found
return repository.findById(id)
    .switchIfEmpty(Mono.error(new EntityNotFoundException("Course", id)))
    .map(this::toOutputDTO);

// Access denied
if (!hasAccess) {
    return Mono.error(new AccessDeniedException("CREATE", "Course"));
}

// Duplicate entity
if (exists) {
    return Mono.error(new DuplicateEntityException("Course", "code", courseCode));
}
```

## Benefits

1. **User-Friendly Errors** - Clear, structured error messages
2. **Field-Level Validation** - Shows exactly which fields failed validation
3. **Swagger Documentation** - Error responses are properly documented
4. **Consistent Format** - All errors follow the same structure
5. **Proper HTTP Status Codes** - Correct status codes for each error type
6. **Debugging Support** - Detailed logging for troubleshooting
7. **Security** - Generic messages for internal errors (no stack traces exposed)

## Testing in Swagger

When testing in Swagger UI, validation errors will now show:
- HTTP 400 status
- Field-specific error messages
- Clear indication of what went wrong
- Structured JSON response

Example: Try creating an entity with missing required fields to see validation errors in action.
