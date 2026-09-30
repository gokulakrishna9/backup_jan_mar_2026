package com.example.controller;

import com.example.dto.CommunityPropertyGroupInputDTO;
import com.example.dto.CommunityPropertyGroupOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.CommunityPropertyGroupService;
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
 * REST Controller for CommunityPropertyGroup endpoints.
 */
@RestController
@RequestMapping("/api/communitypropertygroups")
@RequiredArgsConstructor
@Tag(name = "CommunityPropertyGroup", description = "CommunityPropertyGroup management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class CommunityPropertyGroupController {
    
    private final CommunityPropertyGroupService service;
    
    /**
     * Create a new CommunityPropertyGroup
     */
    @Operation(summary = "Create a new CommunityPropertyGroup", description = "Creates a new CommunityPropertyGroup record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyGroup created successfully",
            content = @Content(schema = @Schema(implementation = CommunityPropertyGroupOutputDTO.class))),
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
    public Mono<CommunityPropertyGroupOutputDTO> create(@Valid @RequestBody CommunityPropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get CommunityPropertyGroup by ID
     */
    @Operation(summary = "Get CommunityPropertyGroup by ID", description = "Retrieves a CommunityPropertyGroup by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyGroup found",
            content = @Content(schema = @Schema(implementation = CommunityPropertyGroupOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CommunityPropertyGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<CommunityPropertyGroupOutputDTO> findById(
            @Parameter(description = "CommunityPropertyGroup ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all CommunityPropertyGroup entities (paginated)
     */
    @Operation(summary = "Get all CommunityPropertyGroup entities (paginated)", description = "Retrieves CommunityPropertyGroup records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of CommunityPropertyGroup entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<CommunityPropertyGroupOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update CommunityPropertyGroup by ID
     */
    @Operation(summary = "Update CommunityPropertyGroup", description = "Updates an existing CommunityPropertyGroup by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyGroup updated successfully",
            content = @Content(schema = @Schema(implementation = CommunityPropertyGroupOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CommunityPropertyGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<CommunityPropertyGroupOutputDTO> update(
            @Parameter(description = "CommunityPropertyGroup ID", required = true) @PathVariable Long id,
            @Valid @RequestBody CommunityPropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete CommunityPropertyGroup by ID
     */
    @Operation(summary = "Delete CommunityPropertyGroup", description = "Deletes a CommunityPropertyGroup by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyGroup deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CommunityPropertyGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "CommunityPropertyGroup ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete CommunityPropertyGroup with justification", description = "Deletes a CommunityPropertyGroup with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyGroup deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CommunityPropertyGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "CommunityPropertyGroup ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}