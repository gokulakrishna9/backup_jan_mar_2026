package com.example.controller;

import com.example.dto.AiInstitutionProfileEvaluationInputDTO;
import com.example.dto.AiInstitutionProfileEvaluationOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.AiInstitutionProfileEvaluationService;
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
 * REST Controller for AiInstitutionProfileEvaluation endpoints.
 */
@RestController
@RequestMapping("/api/aiinstitutionprofileevaluations")
@RequiredArgsConstructor
@Tag(name = "AiInstitutionProfileEvaluation", description = "AiInstitutionProfileEvaluation management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class AiInstitutionProfileEvaluationController {
    
    private final AiInstitutionProfileEvaluationService service;
    
    /**
     * Create a new AiInstitutionProfileEvaluation
     */
    @Operation(summary = "Create a new AiInstitutionProfileEvaluation", description = "Creates a new AiInstitutionProfileEvaluation record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiInstitutionProfileEvaluation created successfully",
            content = @Content(schema = @Schema(implementation = AiInstitutionProfileEvaluationOutputDTO.class))),
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
    public Mono<AiInstitutionProfileEvaluationOutputDTO> create(@Valid @RequestBody AiInstitutionProfileEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get AiInstitutionProfileEvaluation by ID
     */
    @Operation(summary = "Get AiInstitutionProfileEvaluation by ID", description = "Retrieves a AiInstitutionProfileEvaluation by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiInstitutionProfileEvaluation found",
            content = @Content(schema = @Schema(implementation = AiInstitutionProfileEvaluationOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiInstitutionProfileEvaluation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<AiInstitutionProfileEvaluationOutputDTO> findById(
            @Parameter(description = "AiInstitutionProfileEvaluation ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all AiInstitutionProfileEvaluation entities (paginated)
     */
    @Operation(summary = "Get all AiInstitutionProfileEvaluation entities (paginated)", description = "Retrieves AiInstitutionProfileEvaluation records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of AiInstitutionProfileEvaluation entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<AiInstitutionProfileEvaluationOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update AiInstitutionProfileEvaluation by ID
     */
    @Operation(summary = "Update AiInstitutionProfileEvaluation", description = "Updates an existing AiInstitutionProfileEvaluation by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiInstitutionProfileEvaluation updated successfully",
            content = @Content(schema = @Schema(implementation = AiInstitutionProfileEvaluationOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiInstitutionProfileEvaluation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<AiInstitutionProfileEvaluationOutputDTO> update(
            @Parameter(description = "AiInstitutionProfileEvaluation ID", required = true) @PathVariable Long id,
            @Valid @RequestBody AiInstitutionProfileEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete AiInstitutionProfileEvaluation by ID
     */
    @Operation(summary = "Delete AiInstitutionProfileEvaluation", description = "Deletes a AiInstitutionProfileEvaluation by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiInstitutionProfileEvaluation deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiInstitutionProfileEvaluation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "AiInstitutionProfileEvaluation ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete AiInstitutionProfileEvaluation with justification", description = "Deletes a AiInstitutionProfileEvaluation with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiInstitutionProfileEvaluation deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiInstitutionProfileEvaluation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "AiInstitutionProfileEvaluation ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}