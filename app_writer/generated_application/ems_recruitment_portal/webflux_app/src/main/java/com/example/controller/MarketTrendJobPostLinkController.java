package com.example.controller;

import com.example.dto.MarketTrendJobPostLinkInputDTO;
import com.example.dto.MarketTrendJobPostLinkOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.MarketTrendJobPostLinkService;
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
 * REST Controller for MarketTrendJobPostLink endpoints.
 */
@RestController
@RequestMapping("/api/markettrendjobpostlinks")
@RequiredArgsConstructor
@Tag(name = "MarketTrendJobPostLink", description = "MarketTrendJobPostLink management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class MarketTrendJobPostLinkController {
    
    private final MarketTrendJobPostLinkService service;
    
    /**
     * Create a new MarketTrendJobPostLink
     */
    @Operation(summary = "Create a new MarketTrendJobPostLink", description = "Creates a new MarketTrendJobPostLink record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendJobPostLink created successfully",
            content = @Content(schema = @Schema(implementation = MarketTrendJobPostLinkOutputDTO.class))),
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
    public Mono<MarketTrendJobPostLinkOutputDTO> create(@Valid @RequestBody MarketTrendJobPostLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get MarketTrendJobPostLink by ID
     */
    @Operation(summary = "Get MarketTrendJobPostLink by ID", description = "Retrieves a MarketTrendJobPostLink by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendJobPostLink found",
            content = @Content(schema = @Schema(implementation = MarketTrendJobPostLinkOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendJobPostLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<MarketTrendJobPostLinkOutputDTO> findById(
            @Parameter(description = "MarketTrendJobPostLink ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all MarketTrendJobPostLink entities (paginated)
     */
    @Operation(summary = "Get all MarketTrendJobPostLink entities (paginated)", description = "Retrieves MarketTrendJobPostLink records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of MarketTrendJobPostLink entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<MarketTrendJobPostLinkOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update MarketTrendJobPostLink by ID
     */
    @Operation(summary = "Update MarketTrendJobPostLink", description = "Updates an existing MarketTrendJobPostLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendJobPostLink updated successfully",
            content = @Content(schema = @Schema(implementation = MarketTrendJobPostLinkOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendJobPostLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<MarketTrendJobPostLinkOutputDTO> update(
            @Parameter(description = "MarketTrendJobPostLink ID", required = true) @PathVariable Long id,
            @Valid @RequestBody MarketTrendJobPostLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete MarketTrendJobPostLink by ID
     */
    @Operation(summary = "Delete MarketTrendJobPostLink", description = "Deletes a MarketTrendJobPostLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendJobPostLink deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendJobPostLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "MarketTrendJobPostLink ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete MarketTrendJobPostLink with justification", description = "Deletes a MarketTrendJobPostLink with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendJobPostLink deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendJobPostLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "MarketTrendJobPostLink ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}