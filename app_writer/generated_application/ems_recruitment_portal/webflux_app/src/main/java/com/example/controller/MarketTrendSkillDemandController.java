package com.example.controller;

import com.example.dto.MarketTrendSkillDemandInputDTO;
import com.example.dto.MarketTrendSkillDemandOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.MarketTrendSkillDemandService;
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
 * REST Controller for MarketTrendSkillDemand endpoints.
 */
@RestController
@RequestMapping("/api/markettrendskilldemands")
@RequiredArgsConstructor
@Tag(name = "MarketTrendSkillDemand", description = "MarketTrendSkillDemand management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class MarketTrendSkillDemandController {
    
    private final MarketTrendSkillDemandService service;
    
    /**
     * Create a new MarketTrendSkillDemand
     */
    @Operation(summary = "Create a new MarketTrendSkillDemand", description = "Creates a new MarketTrendSkillDemand record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendSkillDemand created successfully",
            content = @Content(schema = @Schema(implementation = MarketTrendSkillDemandOutputDTO.class))),
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
    public Mono<MarketTrendSkillDemandOutputDTO> create(@Valid @RequestBody MarketTrendSkillDemandInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get MarketTrendSkillDemand by ID
     */
    @Operation(summary = "Get MarketTrendSkillDemand by ID", description = "Retrieves a MarketTrendSkillDemand by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendSkillDemand found",
            content = @Content(schema = @Schema(implementation = MarketTrendSkillDemandOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendSkillDemand not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<MarketTrendSkillDemandOutputDTO> findById(
            @Parameter(description = "MarketTrendSkillDemand ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all MarketTrendSkillDemand entities (paginated)
     */
    @Operation(summary = "Get all MarketTrendSkillDemand entities (paginated)", description = "Retrieves MarketTrendSkillDemand records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of MarketTrendSkillDemand entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<MarketTrendSkillDemandOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update MarketTrendSkillDemand by ID
     */
    @Operation(summary = "Update MarketTrendSkillDemand", description = "Updates an existing MarketTrendSkillDemand by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendSkillDemand updated successfully",
            content = @Content(schema = @Schema(implementation = MarketTrendSkillDemandOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendSkillDemand not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<MarketTrendSkillDemandOutputDTO> update(
            @Parameter(description = "MarketTrendSkillDemand ID", required = true) @PathVariable Long id,
            @Valid @RequestBody MarketTrendSkillDemandInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete MarketTrendSkillDemand by ID
     */
    @Operation(summary = "Delete MarketTrendSkillDemand", description = "Deletes a MarketTrendSkillDemand by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendSkillDemand deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendSkillDemand not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "MarketTrendSkillDemand ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete MarketTrendSkillDemand with justification", description = "Deletes a MarketTrendSkillDemand with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendSkillDemand deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendSkillDemand not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "MarketTrendSkillDemand ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}