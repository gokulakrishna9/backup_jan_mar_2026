package com.example.controller;

import com.example.dto.AiMarketTrendPropertyInputDTO;
import com.example.dto.AiMarketTrendPropertyOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.AiMarketTrendPropertyService;
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
 * REST Controller for AiMarketTrendProperty endpoints.
 */
@RestController
@RequestMapping("/api/aimarkettrendpropertys")
@RequiredArgsConstructor
@Tag(name = "AiMarketTrendProperty", description = "AiMarketTrendProperty management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class AiMarketTrendPropertyController {
    
    private final AiMarketTrendPropertyService service;
    
    /**
     * Create a new AiMarketTrendProperty
     */
    @Operation(summary = "Create a new AiMarketTrendProperty", description = "Creates a new AiMarketTrendProperty record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendProperty created successfully",
            content = @Content(schema = @Schema(implementation = AiMarketTrendPropertyOutputDTO.class))),
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
    public Mono<AiMarketTrendPropertyOutputDTO> create(@Valid @RequestBody AiMarketTrendPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get AiMarketTrendProperty by ID
     */
    @Operation(summary = "Get AiMarketTrendProperty by ID", description = "Retrieves a AiMarketTrendProperty by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendProperty found",
            content = @Content(schema = @Schema(implementation = AiMarketTrendPropertyOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendProperty not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<AiMarketTrendPropertyOutputDTO> findById(
            @Parameter(description = "AiMarketTrendProperty ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all AiMarketTrendProperty entities (paginated)
     */
    @Operation(summary = "Get all AiMarketTrendProperty entities (paginated)", description = "Retrieves AiMarketTrendProperty records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of AiMarketTrendProperty entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<AiMarketTrendPropertyOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update AiMarketTrendProperty by ID
     */
    @Operation(summary = "Update AiMarketTrendProperty", description = "Updates an existing AiMarketTrendProperty by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendProperty updated successfully",
            content = @Content(schema = @Schema(implementation = AiMarketTrendPropertyOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendProperty not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<AiMarketTrendPropertyOutputDTO> update(
            @Parameter(description = "AiMarketTrendProperty ID", required = true) @PathVariable Long id,
            @Valid @RequestBody AiMarketTrendPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete AiMarketTrendProperty by ID
     */
    @Operation(summary = "Delete AiMarketTrendProperty", description = "Deletes a AiMarketTrendProperty by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendProperty deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendProperty not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "AiMarketTrendProperty ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete AiMarketTrendProperty with justification", description = "Deletes a AiMarketTrendProperty with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendProperty deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendProperty not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "AiMarketTrendProperty ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}