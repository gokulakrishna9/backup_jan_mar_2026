package com.jobportal.controller;

import com.jobportal.dto.ModuleProgressInputDTO;
import com.jobportal.dto.ModuleProgressOutputDTO;
import com.jobportal.dto.PageResponse;
import com.jobportal.service.ModuleProgressService;
import com.jobportal.exception.ErrorResponse;
import com.jobportal.exception.ValidationErrorResponse;
import com.jobportal.security.EntityTable;
import com.jobportal.security.TableAccess;
import com.jobportal.security.QueryAccess;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import jakarta.validation.Valid;

/**
 * REST Controller for ModuleProgress endpoints.
 */
@RestController
@RequestMapping("/api/module_progresss")
@RequiredArgsConstructor
@Tag(name = "ModuleProgress", description = "ModuleProgress management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class ModuleProgressController {
    
    private final ModuleProgressService service;
    
    /**
     * Create a new ModuleProgress
     */
    @Operation(summary = "Create a new ModuleProgress", description = "Creates a new ModuleProgress record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ModuleProgress created successfully",
            content = @Content(schema = @Schema(implementation = ModuleProgressOutputDTO.class))),
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
    @PostMapping("")
    public Mono<ModuleProgressOutputDTO> create(@Valid @RequestBody ModuleProgressInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get ModuleProgress by ID
     */
    @Operation(summary = "Get ModuleProgress by ID", description = "Retrieves a ModuleProgress by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ModuleProgress found",
            content = @Content(schema = @Schema(implementation = ModuleProgressOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ModuleProgress not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<ModuleProgressOutputDTO> findById(
            @Parameter(description = "ModuleProgress ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all ModuleProgress entities (paginated)
     */
    @Operation(summary = "Get all ModuleProgress entities (paginated)", description = "Retrieves ModuleProgress records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of ModuleProgress entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<ModuleProgressOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update ModuleProgress by ID
     */
    @Operation(summary = "Update ModuleProgress", description = "Updates an existing ModuleProgress by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ModuleProgress updated successfully",
            content = @Content(schema = @Schema(implementation = ModuleProgressOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ModuleProgress not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<ModuleProgressOutputDTO> update(
            @Parameter(description = "ModuleProgress ID", required = true) @PathVariable Long id,
            @Valid @RequestBody ModuleProgressInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete ModuleProgress by ID
     */
    @Operation(summary = "Delete ModuleProgress", description = "Deletes a ModuleProgress by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ModuleProgress deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ModuleProgress not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(
            @Parameter(description = "ModuleProgress ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete ModuleProgress with justification", description = "Deletes a ModuleProgress with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ModuleProgress deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ModuleProgress not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "ModuleProgress ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}