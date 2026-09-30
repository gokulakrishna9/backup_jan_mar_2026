package com.example.controller;

import com.example.dto.AiCommunityPostEvaluationInputDTO;
import com.example.dto.AiCommunityPostEvaluationOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.AiCommunityPostEvaluationService;
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
 * REST Controller for AiCommunityPostEvaluation endpoints.
 */
@RestController
@RequestMapping("/api/aicommunitypostevaluations")
@RequiredArgsConstructor
@Tag(name = "AiCommunityPostEvaluation", description = "AiCommunityPostEvaluation management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class AiCommunityPostEvaluationController {
    
    private final AiCommunityPostEvaluationService service;
    
    /**
     * Create a new AiCommunityPostEvaluation
     */
    @Operation(summary = "Create a new AiCommunityPostEvaluation", description = "Creates a new AiCommunityPostEvaluation record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiCommunityPostEvaluation created successfully",
            content = @Content(schema = @Schema(implementation = AiCommunityPostEvaluationOutputDTO.class))),
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
    public Mono<AiCommunityPostEvaluationOutputDTO> create(@Valid @RequestBody AiCommunityPostEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get AiCommunityPostEvaluation by ID
     */
    @Operation(summary = "Get AiCommunityPostEvaluation by ID", description = "Retrieves a AiCommunityPostEvaluation by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiCommunityPostEvaluation found",
            content = @Content(schema = @Schema(implementation = AiCommunityPostEvaluationOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiCommunityPostEvaluation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<AiCommunityPostEvaluationOutputDTO> findById(
            @Parameter(description = "AiCommunityPostEvaluation ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all AiCommunityPostEvaluation entities (paginated)
     */
    @Operation(summary = "Get all AiCommunityPostEvaluation entities (paginated)", description = "Retrieves AiCommunityPostEvaluation records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of AiCommunityPostEvaluation entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<AiCommunityPostEvaluationOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update AiCommunityPostEvaluation by ID
     */
    @Operation(summary = "Update AiCommunityPostEvaluation", description = "Updates an existing AiCommunityPostEvaluation by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiCommunityPostEvaluation updated successfully",
            content = @Content(schema = @Schema(implementation = AiCommunityPostEvaluationOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiCommunityPostEvaluation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<AiCommunityPostEvaluationOutputDTO> update(
            @Parameter(description = "AiCommunityPostEvaluation ID", required = true) @PathVariable Long id,
            @Valid @RequestBody AiCommunityPostEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete AiCommunityPostEvaluation by ID
     */
    @Operation(summary = "Delete AiCommunityPostEvaluation", description = "Deletes a AiCommunityPostEvaluation by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiCommunityPostEvaluation deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiCommunityPostEvaluation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "AiCommunityPostEvaluation ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete AiCommunityPostEvaluation with justification", description = "Deletes a AiCommunityPostEvaluation with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiCommunityPostEvaluation deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiCommunityPostEvaluation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "AiCommunityPostEvaluation ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}