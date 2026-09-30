package com.example.controller;

import com.example.dto.AiMarketTrendParameterGroupInputDTO;
import com.example.dto.AiMarketTrendParameterGroupOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.AiMarketTrendParameterGroupService;
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
 * REST Controller for AiMarketTrendParameterGroup endpoints.
 */
@RestController
@RequestMapping("/api/aimarkettrendparametergroups")
@RequiredArgsConstructor
@Tag(name = "AiMarketTrendParameterGroup", description = "AiMarketTrendParameterGroup management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class AiMarketTrendParameterGroupController {
    
    private final AiMarketTrendParameterGroupService service;
    
    /**
     * Create a new AiMarketTrendParameterGroup
     */
    @Operation(summary = "Create a new AiMarketTrendParameterGroup", description = "Creates a new AiMarketTrendParameterGroup record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameterGroup created successfully",
            content = @Content(schema = @Schema(implementation = AiMarketTrendParameterGroupOutputDTO.class))),
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
    public Mono<AiMarketTrendParameterGroupOutputDTO> create(@Valid @RequestBody AiMarketTrendParameterGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get AiMarketTrendParameterGroup by ID
     */
    @Operation(summary = "Get AiMarketTrendParameterGroup by ID", description = "Retrieves a AiMarketTrendParameterGroup by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameterGroup found",
            content = @Content(schema = @Schema(implementation = AiMarketTrendParameterGroupOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendParameterGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<AiMarketTrendParameterGroupOutputDTO> findById(
            @Parameter(description = "AiMarketTrendParameterGroup ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all AiMarketTrendParameterGroup entities (paginated)
     */
    @Operation(summary = "Get all AiMarketTrendParameterGroup entities (paginated)", description = "Retrieves AiMarketTrendParameterGroup records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of AiMarketTrendParameterGroup entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<AiMarketTrendParameterGroupOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update AiMarketTrendParameterGroup by ID
     */
    @Operation(summary = "Update AiMarketTrendParameterGroup", description = "Updates an existing AiMarketTrendParameterGroup by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameterGroup updated successfully",
            content = @Content(schema = @Schema(implementation = AiMarketTrendParameterGroupOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendParameterGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<AiMarketTrendParameterGroupOutputDTO> update(
            @Parameter(description = "AiMarketTrendParameterGroup ID", required = true) @PathVariable Long id,
            @Valid @RequestBody AiMarketTrendParameterGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete AiMarketTrendParameterGroup by ID
     */
    @Operation(summary = "Delete AiMarketTrendParameterGroup", description = "Deletes a AiMarketTrendParameterGroup by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameterGroup deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendParameterGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "AiMarketTrendParameterGroup ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete AiMarketTrendParameterGroup with justification", description = "Deletes a AiMarketTrendParameterGroup with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameterGroup deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendParameterGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "AiMarketTrendParameterGroup ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}