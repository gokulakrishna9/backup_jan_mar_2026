"""Quick verification script for document_collection_templates.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from templates.document_collection_templates import DocumentCollectionTemplates as T

pkg = "com.example"
name = "AuditLog"
table = "audit_log_docs"

e = T.generate_collection_entity(pkg, name, table)
assert '@Table("audit_log_docs")' in e
assert "private JsonNode content;" in e
assert "private Long id;" in e
assert "private LocalDateTime createdAt;" in e
assert "private LocalDateTime updatedAt;" in e
print("Entity: OK")

r = T.generate_collection_repository(pkg, name, table)
assert "ReactiveCrudRepository<AuditLog, Long>" in r
assert "JSON_EXTRACT" in r
assert "findByContentPath" in r
print("Repository: OK")

s = T.generate_collection_service(pkg, name, table)
assert "Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN" in s
assert "CREATE" in s and "READ" in s and "UPDATE" in s and "DELETE" in s
assert "SecurityContextHolder" in s
assert "Mono<AuditLog>" in s
assert "Flux<AuditLog>" in s
print("Service: OK")

c = T.generate_collection_controller(pkg, name, table)
assert "@PostMapping" in c
assert '@GetMapping("/{id}")' in c
assert '@PutMapping("/{id}")' in c
assert '@DeleteMapping("/{id}")' in c
assert '@GetMapping("/search")' in c
assert "jsonPath" in c and "value" in c
print("Controller: OK")

i = T.generate_collection_input_dto(pkg, name, table)
assert "JsonNode content" in i
assert "AuditLogInputDTO" in i
print("InputDTO: OK")

o = T.generate_collection_output_dto(pkg, name, table)
assert "JsonNode content" in o
assert "Long id" in o
assert "LocalDateTime createdAt" in o
assert "LocalDateTime updatedAt" in o
assert "AuditLogOutputDTO" in o
print("OutputDTO: OK")

print("\nAll assertions passed!")
