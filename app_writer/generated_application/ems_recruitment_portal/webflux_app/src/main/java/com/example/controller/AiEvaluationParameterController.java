package com.example.controller;

import com.example.dto.AiEvaluationParameterInputDTO;
import com.example.dto.AiEvaluationParameterOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.AiEvaluationParameterService;
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
 * REST Controller for AiEvaluationParameter endpoints.
 */
@RestController
@RequestMapping("/api/aievaluationparameters")
@RequiredArgsConstructor
@Tag(name = "AiEvaluationParameter", description = "AiEvaluationParameter management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class AiEvaluationParameterController {
    
    private final AiEvaluationParameterService service;
    
    /**
     * Create a new AiEvaluationParameter
     */
    @Operation(summary = "Create a new AiEvaluationParameter", description = "Creates a new AiEvaluationParameter record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiEvaluationParameter created successfully",
            content = @Content(schema = @Schema(implementation = AiEvaluationParameterOutputDTO.class))),
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
    public Mono<AiEvaluationParameterOutputDTO> create(@Valid @RequestBody AiEvaluationParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get AiEvaluationParameter by ID
     */
    @Operation(summary = "Get AiEvaluationParameter by ID", description = "Retrieves a AiEvaluationParameter by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiEvaluationParameter found",
            content = @Content(schema = @Schema(implementation = AiEvaluationParameterOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiEvaluationParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<AiEvaluationParameterOutputDTO> findById(
            @Parameter(description = "AiEvaluationParameter ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all AiEvaluationParameter entities (paginated)
     */
    @Operation(summary = "Get all AiEvaluationParameter entities (paginated)", description = "Retrieves AiEvaluationParameter records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of AiEvaluationParameter entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<AiEvaluationParameterOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update AiEvaluationParameter by ID
     */
    @Operation(summary = "Update AiEvaluationParameter", description = "Updates an existing AiEvaluationParameter by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiEvaluationParameter updated successfully",
            content = @Content(schema = @Schema(implementation = AiEvaluationParameterOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiEvaluationParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<AiEvaluationParameterOutputDTO> update(
            @Parameter(description = "AiEvaluationParameter ID", required = true) @PathVariable Long id,
            @Valid @RequestBody AiEvaluationParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete AiEvaluationParameter by ID
     */
    @Operation(summary = "Delete AiEvaluationParameter", description = "Deletes a AiEvaluationParameter by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiEvaluationParameter deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiEvaluationParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "AiEvaluationParameter ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete AiEvaluationParameter with justification", description = "Deletes a AiEvaluationParameter with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiEvaluationParameter deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiEvaluationParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "AiEvaluationParameter ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}