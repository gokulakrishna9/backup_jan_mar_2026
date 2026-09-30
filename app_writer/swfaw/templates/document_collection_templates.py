"""Document collection templates - templates for per-collection entity, repository, service, controller, and DTOs."""


class DocumentCollectionTemplates:
    """Templates for document collection Java code generation.

    Each method takes package_name, collection_name, and table_name,
    and returns a Java source file as an f-string.
    """

    @staticmethod
    def generate_collection_entity(package_name: str, collection_name: str, table_name: str) -> str:
        """Generate document collection entity with @Table, fields id/content/createdAt/updatedAt."""
        return f"""package {package_name}.document;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity representing a schema-less document in the {table_name} table.
 * Stores arbitrary JSON content with audit timestamps.
 */
@Table("{table_name}")
public class {collection_name} {{

    @Id
    private Long id;

    @Column("content")
    private JsonNode content;

    @Column("created_at")
    private LocalDateTime createdAt;

    @Column("updated_at")
    private LocalDateTime updatedAt;

    // Constructors
    public {collection_name}() {{
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }}

    // Getters and Setters
    public Long getId() {{
        return id;
    }}

    public void setId(Long id) {{
        this.id = id;
    }}

    public JsonNode getContent() {{
        return content;
    }}

    public void setContent(JsonNode content) {{
        this.content = content;
    }}

    public LocalDateTime getCreatedAt() {{
        return createdAt;
    }}

    public void setCreatedAt(LocalDateTime createdAt) {{
        this.createdAt = createdAt;
    }}

    public LocalDateTime getUpdatedAt() {{
        return updatedAt;
    }}

    public void setUpdatedAt(LocalDateTime updatedAt) {{
        this.updatedAt = updatedAt;
    }}
}}
"""

    @staticmethod
    def generate_collection_repository(package_name: str, collection_name: str, table_name: str) -> str:
        """Generate document collection repository with findByContentPath using JSON_EXTRACT."""
        return f"""package {package_name}.document;

import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

/**
 * Repository for {collection_name} document collection.
 * Provides reactive CRUD and JSON path search via MySQL JSON_EXTRACT.
 */
@Repository
public interface {collection_name}Repository extends ReactiveCrudRepository<{collection_name}, Long> {{

    @Query("SELECT * FROM {table_name} WHERE JSON_EXTRACT(content, :jsonPath) = :value")
    Flux<{collection_name}> findByContentPath(String jsonPath, String value);
}}
"""

    @staticmethod
    def generate_collection_service(package_name: str, collection_name: str, table_name: str) -> str:
        """Generate document collection service with CRUD + auth checks returning reactive types."""
        lower_name = collection_name[0].lower() + collection_name[1:]
        return f"""package {package_name}.document;

import {package_name}.security.SecurityContextHolder;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;

/**
 * Service for {collection_name} document collection.
 * Provides create, findById, findAll (paginated), update, delete operations.
 * Enforces row-level authorization via SecurityContextHolder.
 */
@Service
public class {collection_name}Service {{

    private final {collection_name}Repository {lower_name}Repository;
    private final SecurityContextHolder securityContextHolder;

    public {collection_name}Service({collection_name}Repository {lower_name}Repository,
                              SecurityContextHolder securityContextHolder) {{
        this.{lower_name}Repository = {lower_name}Repository;
        this.securityContextHolder = securityContextHolder;
    }}

    /**
     * Create a new document in the {collection_name} collection.
     * Requires CREATE permission on the collection table.
     */
    public Mono<{collection_name}> create({collection_name}InputDTO inputDTO) {{
        return securityContextHolder.getCurrentUser()
            .flatMap(user -> securityContextHolder.checkPermission(user, "{table_name}", null, "CREATE")
                .flatMap(allowed -> {{
                    if (!allowed) {{
                        return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                            "Access denied: CREATE on {table_name}"));
                    }}
                    {collection_name} entity = new {collection_name}();
                    entity.setContent(inputDTO.getContent());
                    entity.setCreatedAt(LocalDateTime.now());
                    entity.setUpdatedAt(LocalDateTime.now());
                    return {lower_name}Repository.save(entity);
                }}));
    }}

    /**
     * Find a document by ID.
     * Requires READ permission on the collection table.
     */
    public Mono<{collection_name}> findById(Long id) {{
        return securityContextHolder.getCurrentUser()
            .flatMap(user -> securityContextHolder.checkPermission(user, "{table_name}", null, "READ")
                .flatMap(allowed -> {{
                    if (!allowed) {{
                        return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                            "Access denied: READ on {table_name}"));
                    }}
                    return {lower_name}Repository.findById(id)
                        .switchIfEmpty(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND,
                            "{collection_name} not found: " + id)));
                }}));
    }}

    /**
     * Find all documents with pagination.
     * Requires READ permission on the collection table.
     */
    public Flux<{collection_name}> findAll() {{
        return securityContextHolder.getCurrentUser()
            .flatMapMany(user -> securityContextHolder.checkPermission(user, "{table_name}", null, "READ")
                .flatMapMany(allowed -> {{
                    if (!allowed) {{
                        return Flux.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                            "Access denied: READ on {table_name}"));
                    }}
                    return {lower_name}Repository.findAll();
                }}));
    }}

    /**
     * Update an existing document by ID.
     * Requires UPDATE permission on the collection table.
     */
    public Mono<{collection_name}> update(Long id, {collection_name}InputDTO inputDTO) {{
        return securityContextHolder.getCurrentUser()
            .flatMap(user -> securityContextHolder.checkPermission(user, "{table_name}", null, "UPDATE")
                .flatMap(allowed -> {{
                    if (!allowed) {{
                        return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                            "Access denied: UPDATE on {table_name}"));
                    }}
                    return {lower_name}Repository.findById(id)
                        .switchIfEmpty(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND,
                            "{collection_name} not found: " + id)))
                        .flatMap(existing -> {{
                            existing.setContent(inputDTO.getContent());
                            existing.setUpdatedAt(LocalDateTime.now());
                            return {lower_name}Repository.save(existing);
                        }});
                }}));
    }}

    /**
     * Delete a document by ID.
     * Requires DELETE permission on the collection table.
     */
    public Mono<Void> delete(Long id) {{
        return securityContextHolder.getCurrentUser()
            .flatMap(user -> securityContextHolder.checkPermission(user, "{table_name}", null, "DELETE")
                .flatMap(allowed -> {{
                    if (!allowed) {{
                        return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                            "Access denied: DELETE on {table_name}"));
                    }}
                    return {lower_name}Repository.findById(id)
                        .switchIfEmpty(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND,
                            "{collection_name} not found: " + id)))
                        .flatMap(entity -> {lower_name}Repository.delete(entity));
                }}));
    }}

    /**
     * Search documents by JSON path and value.
     * Requires READ permission on the collection table.
     */
    public Flux<{collection_name}> searchByPath(String jsonPath, String value) {{
        return securityContextHolder.getCurrentUser()
            .flatMapMany(user -> securityContextHolder.checkPermission(user, "{table_name}", null, "READ")
                .flatMapMany(allowed -> {{
                    if (!allowed) {{
                        return Flux.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                            "Access denied: READ on {table_name}"));
                    }}
                    return {lower_name}Repository.findByContentPath(jsonPath, value);
                }}));
    }}
}}
"""

    @staticmethod
    def generate_collection_controller(package_name: str, collection_name: str, table_name: str) -> str:
        """Generate document collection controller with CRUD + search endpoints."""
        lower_name = collection_name[0].lower() + collection_name[1:]
        # Build base path from collection name (camelCase to kebab-case-like lowercase)
        base_path = lower_name
        return f"""package {package_name}.document;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * REST controller for {collection_name} document collection.
 * Provides CRUD endpoints and JSON path search.
 */
@RestController
@RequestMapping("/api/{base_path}")
public class {collection_name}Controller {{

    private final {collection_name}Service {lower_name}Service;

    public {collection_name}Controller({collection_name}Service {lower_name}Service) {{
        this.{lower_name}Service = {lower_name}Service;
    }}

    /**
     * Create a new document.
     * POST /api/{base_path}
     */
    @PostMapping
    public Mono<{collection_name}OutputDTO> create(@RequestBody {collection_name}InputDTO inputDTO) {{
        return {lower_name}Service.create(inputDTO)
            .map(this::toOutputDTO);
    }}

    /**
     * Get a document by ID.
     * GET /api/{base_path}/{{id}}
     */
    @GetMapping("/{{id}}")
    public Mono<{collection_name}OutputDTO> findById(@PathVariable Long id) {{
        return {lower_name}Service.findById(id)
            .map(this::toOutputDTO);
    }}

    /**
     * Get all documents (paginated).
     * GET /api/{base_path}
     */
    @GetMapping
    public Flux<{collection_name}OutputDTO> findAll() {{
        return {lower_name}Service.findAll()
            .map(this::toOutputDTO);
    }}

    /**
     * Update a document by ID.
     * PUT /api/{base_path}/{{id}}
     */
    @PutMapping("/{{id}}")
    public Mono<{collection_name}OutputDTO> update(@PathVariable Long id, @RequestBody {collection_name}InputDTO inputDTO) {{
        return {lower_name}Service.update(id, inputDTO)
            .map(this::toOutputDTO);
    }}

    /**
     * Delete a document by ID.
     * DELETE /api/{base_path}/{{id}}
     */
    @DeleteMapping("/{{id}}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(@PathVariable Long id) {{
        return {lower_name}Service.delete(id);
    }}

    /**
     * Search documents by JSON path and value.
     * GET /api/{base_path}/search?jsonPath=$.name&value=test
     */
    @GetMapping("/search")
    public Flux<{collection_name}OutputDTO> search(
            @RequestParam String jsonPath,
            @RequestParam String value) {{
        return {lower_name}Service.searchByPath(jsonPath, value)
            .map(this::toOutputDTO);
    }}

    private {collection_name}OutputDTO toOutputDTO({collection_name} entity) {{
        {collection_name}OutputDTO dto = new {collection_name}OutputDTO();
        dto.setId(entity.getId());
        dto.setContent(entity.getContent());
        dto.setCreatedAt(entity.getCreatedAt());
        dto.setUpdatedAt(entity.getUpdatedAt());
        return dto;
    }}
}}
"""

    @staticmethod
    def generate_collection_input_dto(package_name: str, collection_name: str, table_name: str) -> str:
        """Generate document collection input DTO with JsonNode content field."""
        return f"""package {package_name}.document;

import com.fasterxml.jackson.databind.JsonNode;

/**
 * Input DTO for creating/updating {collection_name} documents.
 * Contains the JSON content payload.
 */
public class {collection_name}InputDTO {{

    private JsonNode content;

    // Constructors
    public {collection_name}InputDTO() {{
    }}

    // Getters and Setters
    public JsonNode getContent() {{
        return content;
    }}

    public void setContent(JsonNode content) {{
        this.content = content;
    }}
}}
"""

    @staticmethod
    def generate_collection_output_dto(package_name: str, collection_name: str, table_name: str) -> str:
        """Generate document collection output DTO with id, content, createdAt, updatedAt."""
        return f"""package {package_name}.document;

import com.fasterxml.jackson.databind.JsonNode;
import java.time.LocalDateTime;

/**
 * Output DTO for {collection_name} documents.
 * Contains id, JSON content, and audit timestamps.
 */
public class {collection_name}OutputDTO {{

    private Long id;
    private JsonNode content;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // Constructors
    public {collection_name}OutputDTO() {{
    }}

    // Getters and Setters
    public Long getId() {{
        return id;
    }}

    public void setId(Long id) {{
        this.id = id;
    }}

    public JsonNode getContent() {{
        return content;
    }}

    public void setContent(JsonNode content) {{
        this.content = content;
    }}

    public LocalDateTime getCreatedAt() {{
        return createdAt;
    }}

    public void setCreatedAt(LocalDateTime createdAt) {{
        this.createdAt = createdAt;
    }}

    public LocalDateTime getUpdatedAt() {{
        return updatedAt;
    }}

    public void setUpdatedAt(LocalDateTime updatedAt) {{
        this.updatedAt = updatedAt;
    }}
}}
"""
