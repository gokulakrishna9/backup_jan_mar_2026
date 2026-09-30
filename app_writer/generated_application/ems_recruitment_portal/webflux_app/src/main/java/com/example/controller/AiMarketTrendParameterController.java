package com.example.controller;

import com.example.dto.AiMarketTrendParameterInputDTO;
import com.example.dto.AiMarketTrendParameterOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.AiMarketTrendParameterService;
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
 * REST Controller for AiMarketTrendParameter endpoints.
 */
@RestController
@RequestMapping("/api/aimarkettrendparameters")
@RequiredArgsConstructor
@Tag(name = "AiMarketTrendParameter", description = "AiMarketTrendParameter management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class AiMarketTrendParameterController {
    
    private final AiMarketTrendParameterService service;
    
    /**
     * Create a new AiMarketTrendParameter
     */
    @Operation(summary = "Create a new AiMarketTrendParameter", description = "Creates a new AiMarketTrendParameter record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameter created successfully",
            content = @Content(schema = @Schema(implementation = AiMarketTrendParameterOutputDTO.class))),
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
    public Mono<AiMarketTrendParameterOutputDTO> create(@Valid @RequestBody AiMarketTrendParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get AiMarketTrendParameter by ID
     */
    @Operation(summary = "Get AiMarketTrendParameter by ID", description = "Retrieves a AiMarketTrendParameter by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameter found",
            content = @Content(schema = @Schema(implementation = AiMarketTrendParameterOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<AiMarketTrendParameterOutputDTO> findById(
            @Parameter(description = "AiMarketTrendParameter ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all AiMarketTrendParameter entities (paginated)
     */
    @Operation(summary = "Get all AiMarketTrendParameter entities (paginated)", description = "Retrieves AiMarketTrendParameter records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of AiMarketTrendParameter entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<AiMarketTrendParameterOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update AiMarketTrendParameter by ID
     */
    @Operation(summary = "Update AiMarketTrendParameter", description = "Updates an existing AiMarketTrendParameter by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameter updated successfully",
            content = @Content(schema = @Schema(implementation = AiMarketTrendParameterOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<AiMarketTrendParameterOutputDTO> update(
            @Parameter(description = "AiMarketTrendParameter ID", required = true) @PathVariable Long id,
            @Valid @RequestBody AiMarketTrendParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete AiMarketTrendParameter by ID
     */
    @Operation(summary = "Delete AiMarketTrendParameter", description = "Deletes a AiMarketTrendParameter by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameter deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "AiMarketTrendParameter ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete AiMarketTrendParameter with justification", description = "Deletes a AiMarketTrendParameter with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiMarketTrendParameter deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiMarketTrendParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "AiMarketTrendParameter ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}