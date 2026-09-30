package com.example.controller;

import com.example.dto.MarketTrendInstitutionLinkInputDTO;
import com.example.dto.MarketTrendInstitutionLinkOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.MarketTrendInstitutionLinkService;
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
 * REST Controller for MarketTrendInstitutionLink endpoints.
 */
@RestController
@RequestMapping("/api/markettrendinstitutionlinks")
@RequiredArgsConstructor
@Tag(name = "MarketTrendInstitutionLink", description = "MarketTrendInstitutionLink management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class MarketTrendInstitutionLinkController {
    
    private final MarketTrendInstitutionLinkService service;
    
    /**
     * Create a new MarketTrendInstitutionLink
     */
    @Operation(summary = "Create a new MarketTrendInstitutionLink", description = "Creates a new MarketTrendInstitutionLink record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendInstitutionLink created successfully",
            content = @Content(schema = @Schema(implementation = MarketTrendInstitutionLinkOutputDTO.class))),
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
    public Mono<MarketTrendInstitutionLinkOutputDTO> create(@Valid @RequestBody MarketTrendInstitutionLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get MarketTrendInstitutionLink by ID
     */
    @Operation(summary = "Get MarketTrendInstitutionLink by ID", description = "Retrieves a MarketTrendInstitutionLink by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendInstitutionLink found",
            content = @Content(schema = @Schema(implementation = MarketTrendInstitutionLinkOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendInstitutionLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<MarketTrendInstitutionLinkOutputDTO> findById(
            @Parameter(description = "MarketTrendInstitutionLink ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all MarketTrendInstitutionLink entities (paginated)
     */
    @Operation(summary = "Get all MarketTrendInstitutionLink entities (paginated)", description = "Retrieves MarketTrendInstitutionLink records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of MarketTrendInstitutionLink entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<MarketTrendInstitutionLinkOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update MarketTrendInstitutionLink by ID
     */
    @Operation(summary = "Update MarketTrendInstitutionLink", description = "Updates an existing MarketTrendInstitutionLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendInstitutionLink updated successfully",
            content = @Content(schema = @Schema(implementation = MarketTrendInstitutionLinkOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendInstitutionLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<MarketTrendInstitutionLinkOutputDTO> update(
            @Parameter(description = "MarketTrendInstitutionLink ID", required = true) @PathVariable Long id,
            @Valid @RequestBody MarketTrendInstitutionLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete MarketTrendInstitutionLink by ID
     */
    @Operation(summary = "Delete MarketTrendInstitutionLink", description = "Deletes a MarketTrendInstitutionLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendInstitutionLink deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendInstitutionLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "MarketTrendInstitutionLink ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete MarketTrendInstitutionLink with justification", description = "Deletes a MarketTrendInstitutionLink with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "MarketTrendInstitutionLink deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "MarketTrendInstitutionLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "MarketTrendInstitutionLink ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}