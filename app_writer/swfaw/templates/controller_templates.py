"""Controller templates for code generation."""


class ControllerTemplates:
    """Templates for controller class generation."""
    
    CONTROLLER_TEMPLATE = """package {{ packageName }};

import {{ dtoPackage }}.{{ entityName }}InputDTO;
import {{ dtoPackage }}.{{ entityName }}OutputDTO;
import {{ dtoPackage }}.PageResponse;
import {{ servicePackage }}.{{ serviceName }};
import {{ exceptionPackage }}.ErrorResponse;
import {{ exceptionPackage }}.ValidationErrorResponse;
import {{ securityPackage }}.EntityTable;
import {{ securityPackage }}.TableAccess;
import {{ securityPackage }}.QueryAccess;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.*;
{% if corsConfig.enabled %}import org.springframework.web.bind.annotation.CrossOrigin;
{% endif %}{% if hasActivityTracking %}import org.springframework.web.server.ServerWebExchange;
{% endif %}import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import jakarta.validation.Valid;

/**
 * REST Controller for {{ entityName }} endpoints.
 */
@RestController
@RequestMapping("{{ basePath }}")
@RequiredArgsConstructor
@Tag(name = "{{ entityName }}", description = "{{ entityName }} management APIs")
@EntityTable("{{ tableName }}")
{% if corsConfig.enabled %}@CrossOrigin(
    origins = { {% for origin in corsConfig.allowedOrigins %}"{{ origin }}"{% if not loop.last %}, {% endif %}{% endfor %} },
    methods = { {% for method in corsConfig.allowedMethods %}RequestMethod.{{ method }}{% if not loop.last %}, {% endif %}{% endfor %} },
    allowedHeaders = { {% for header in corsConfig.allowedHeaders %}"{{ header }}"{% if not loop.last %}, {% endif %}{% endfor %} },
    maxAge = {{ corsConfig.maxAge }}
)
{% endif %}public class {{ className }} {
    
    private final {{ serviceName }} service;
{% if endpoints.create and endpoints.create.enabled %}    
    /**
     * Create a new {{ entityName }}
     */
    @Operation(summary = "Create a new {{ entityName }}", description = "Creates a new {{ entityName }} record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "{{ entityName }} created successfully",
            content = @Content(schema = @Schema(implementation = {{ entityName }}OutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "409", description = "Conflict - duplicate entity",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "CREATE")
    @PostMapping("{{ endpoints.create.path }}")
    public Mono<{{ entityName }}OutputDTO> create(@Valid @RequestBody {{ entityName }}InputDTO inputDTO{% if hasActivityTracking %}, ServerWebExchange exchange{% endif %}) {
        return service.create(inputDTO{% if hasActivityTracking %}, exchange{% endif %});
    }
{% endif %}{% if endpoints.getById and endpoints.getById.enabled %}    
    /**
     * Get {{ entityName }} by ID
     */
    @Operation(summary = "Get {{ entityName }} by ID", description = "Retrieves a {{ entityName }} by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "{{ entityName }} found",
            content = @Content(schema = @Schema(implementation = {{ entityName }}OutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "{{ entityName }} not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("{{ endpoints.getById.path }}")
    public Mono<{{ entityName }}OutputDTO> findById(
            @Parameter(description = "{{ entityName }} ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
{% endif %}{% if endpoints.getAll and endpoints.getAll.enabled %}    
    /**
     * Get all {{ entityName }} entities (paginated)
     */
    @Operation(summary = "Get all {{ entityName }} entities (paginated)", description = "Retrieves {{ entityName }} records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of {{ entityName }} entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("{{ endpoints.getAll.path }}")
    public Mono<PageResponse<{{ entityName }}OutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "{{ endpoints.getAll.defaultPageSize | default(20) }}") int size) {
        return service.findAllPaged(page, size);
    }
{% endif %}{% if endpoints['update'] and endpoints['update'].enabled %}    
    /**
     * Update {{ entityName }} by ID
     */
    @Operation(summary = "Update {{ entityName }}", description = "Updates an existing {{ entityName }} by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "{{ entityName }} updated successfully",
            content = @Content(schema = @Schema(implementation = {{ entityName }}OutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "{{ entityName }} not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("{{ endpoints['update'].path }}")
    public Mono<{{ entityName }}OutputDTO> update(
            @Parameter(description = "{{ entityName }} ID", required = true) @PathVariable Long id,
            @Valid @RequestBody {{ entityName }}InputDTO inputDTO{% if hasActivityTracking %}, ServerWebExchange exchange{% endif %}) {
        return service.update(id, inputDTO{% if hasActivityTracking %}, exchange{% endif %});
    }
{% endif %}{% if endpoints.delete and endpoints.delete.enabled %}    
    /**
     * Delete {{ entityName }} by ID
     */
    @Operation(summary = "Delete {{ entityName }}", description = "Deletes a {{ entityName }} by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "{{ entityName }} deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "{{ entityName }} not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("{{ endpoints.delete.path }}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(
            @Parameter(description = "{{ entityName }} ID", required = true) @PathVariable Long id{% if hasActivityTracking %}, ServerWebExchange exchange{% endif %}) {
        return service.delete(id{% if hasActivityTracking %}, exchange{% endif %});
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete {{ entityName }} with justification", description = "Deletes a {{ entityName }} with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "{{ entityName }} deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "{{ entityName }} not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("{{ endpoints.delete.path }}/with-justification")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "{{ entityName }} ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification{% if hasActivityTracking %},
            ServerWebExchange exchange{% endif %}) {
        return service.deleteWithJustification(id, justification{% if hasActivityTracking %}, exchange{% endif %});
    }
{% endif %}{% if singleRecordPerUser %}    
    /**
     * Get the current user's own {{ entityName }} record (single-record-per-user)
     */
    @Operation(summary = "Get my {{ entityName }}", description = "Retrieves the current authenticated user's own {{ entityName }} record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "{{ entityName }} found",
            content = @Content(schema = @Schema(implementation = {{ entityName }}OutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "No {{ entityName }} record found for current user",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/me")
    public Mono<{{ entityName }}OutputDTO> findMyRecord() {
        return service.findMyRecord();
    }
{% endif %}{% for customEndpoint in customEndpoints %}    
    /**
     * {{ customEndpoint.description }}
     */
    @Operation(summary = "{{ customEndpoint.description }}")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Success",
            content = @Content(schema = @Schema(implementation = {{ entityName }}OutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "{{ entityName }} not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
{% if customEndpoint.accessLevel == 'ROLE_BASED' %}    @QueryAccess(queryName = "{{ customEndpoint.queryName }}")
{% endif %}    @{{ customEndpoint.httpMethod | capitalize }}Mapping("{{ customEndpoint.path }}")
    public Mono<{{ entityName }}OutputDTO> {{ customEndpoint.methodName }}({% if '{id}' in customEndpoint.path %}@Parameter(description = "{{ entityName }} ID", required = true) @PathVariable Long id{% endif %}) {
        return service.{{ customEndpoint.methodName }}({% if '{id}' in customEndpoint.path %}id{% endif %});
    }
{% endfor %}}
"""
