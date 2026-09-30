package com.example.controller;

import com.example.dto.CoursePropertyGroupInputDTO;
import com.example.dto.CoursePropertyGroupOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.CoursePropertyGroupService;
import com.example.exception.ErrorResponse;
import com.example.exception.ValidationErrorResponse;
import com.example.security.EntityTable;
import com.example.security.TableAccess;
import com.example.security.QueryAccess;
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
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import jakarta.validation.Valid;

/**
 * REST Controller for CoursePropertyGroup endpoints.
 */
@RestController
@RequestMapping("/api/coursepropertygroups")
@RequiredArgsConstructor
@Tag(name = "CoursePropertyGroup", description = "CoursePropertyGroup management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class CoursePropertyGroupController {
    
    private final CoursePropertyGroupService service;
    
    /**
     * Create a new CoursePropertyGroup
     */
    @Operation(summary = "Create a new CoursePropertyGroup", description = "Creates a new CoursePropertyGroup record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CoursePropertyGroup created successfully",
            content = @Content(schema = @Schema(implementation = CoursePropertyGroupOutputDTO.class))),
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
    public Mono<CoursePropertyGroupOutputDTO> create(@Valid @RequestBody CoursePropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get CoursePropertyGroup by ID
     */
    @Operation(summary = "Get CoursePropertyGroup by ID", description = "Retrieves a CoursePropertyGroup by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CoursePropertyGroup found",
            content = @Content(schema = @Schema(implementation = CoursePropertyGroupOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CoursePropertyGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<CoursePropertyGroupOutputDTO> findById(
            @Parameter(description = "CoursePropertyGroup ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all CoursePropertyGroup entities (paginated)
     */
    @Operation(summary = "Get all CoursePropertyGroup entities (paginated)", description = "Retrieves CoursePropertyGroup records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of CoursePropertyGroup entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<CoursePropertyGroupOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update CoursePropertyGroup by ID
     */
    @Operation(summary = "Update CoursePropertyGroup", description = "Updates an existing CoursePropertyGroup by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CoursePropertyGroup updated successfully",
            content = @Content(schema = @Schema(implementation = CoursePropertyGroupOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CoursePropertyGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<CoursePropertyGroupOutputDTO> update(
            @Parameter(description = "CoursePropertyGroup ID", required = true) @PathVariable Long id,
            @Valid @RequestBody CoursePropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete CoursePropertyGroup by ID
     */
    @Operation(summary = "Delete CoursePropertyGroup", description = "Deletes a CoursePropertyGroup by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CoursePropertyGroup deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CoursePropertyGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "CoursePropertyGroup ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete CoursePropertyGroup with justification", description = "Deletes a CoursePropertyGroup with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CoursePropertyGroup deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CoursePropertyGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "CoursePropertyGroup ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}