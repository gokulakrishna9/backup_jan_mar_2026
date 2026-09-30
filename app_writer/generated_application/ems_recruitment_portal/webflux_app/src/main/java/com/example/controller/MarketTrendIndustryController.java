package com.example.controller;

import com.example.dto.MarketTrendIndustryInputDTO;
import com.example.dto.MarketTrendIndustryOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.MarketTrendIndustryService;
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
 * REST Controller for MarketTrendIndustry endpoints.
 */
@RestController
@RequestMapping("/api/markettrendindustrys")
@RequiredArgsConstructor
@Tag(name = "MarketTrendIndustry", description = "MarketTrendIndustry management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class MarketTrendIndustryController {
    
    private final MarketTrendIndustryService service;
    
    /**
     * Create a new MarketTrendIndustry
     */
    @Operation(summary = "Create a new MarketTrendIndustry", description = "Creates a new MarketTrendIndustry record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendIndustry created successfully",
            content = @Content(schema = @Schema(implementation = MarketTrendIndustryOutputDTO.class))),
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
    public Mono<MarketTrendIndustryOutputDTO> create(@Valid @RequestBody MarketTrendIndustryInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get MarketTrendIndustry by ID
     */
    @Operation(summary = "Get MarketTrendIndustry by ID", description = "Retrieves a MarketTrendIndustry by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendIndustry found",
            content = @Content(schema = @Schema(implementation = MarketTrendIndustryOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendIndustry not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<MarketTrendIndustryOutputDTO> findById(
            @Parameter(description = "MarketTrendIndustry ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all MarketTrendIndustry entities (paginated)
     */
    @Operation(summary = "Get all MarketTrendIndustry entities (paginated)", description = "Retrieves MarketTrendIndustry records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of MarketTrendIndustry entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<MarketTrendIndustryOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update MarketTrendIndustry by ID
     */
    @Operation(summary = "Update MarketTrendIndustry", description = "Updates an existing MarketTrendIndustry by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendIndustry updated successfully",
            content = @Content(schema = @Schema(implementation = MarketTrendIndustryOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendIndustry not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<MarketTrendIndustryOutputDTO> update(
            @Parameter(description = "MarketTrendIndustry ID", required = true) @PathVariable Long id,
            @Valid @RequestBody MarketTrendIndustryInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete MarketTrendIndustry by ID
     */
    @Operation(summary = "Delete MarketTrendIndustry", description = "Deletes a MarketTrendIndustry by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendIndustry deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendIndustry not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "MarketTrendIndustry ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete MarketTrendIndustry with justification", description = "Deletes a MarketTrendIndustry with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendIndustry deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendIndustry not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "MarketTrendIndustry ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}