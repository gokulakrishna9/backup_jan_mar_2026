package com.example.controller;

import com.example.dto.AiUserProfileEvaluationParameterInputDTO;
import com.example.dto.AiUserProfileEvaluationParameterOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.AiUserProfileEvaluationParameterService;
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
 * REST Controller for AiUserProfileEvaluationParameter endpoints.
 */
@RestController
@RequestMapping("/api/aiuserprofileevaluationparameters")
@RequiredArgsConstructor
@Tag(name = "AiUserProfileEvaluationParameter", description = "AiUserProfileEvaluationParameter management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class AiUserProfileEvaluationParameterController {
    
    private final AiUserProfileEvaluationParameterService service;
    
    /**
     * Create a new AiUserProfileEvaluationParameter
     */
    @Operation(summary = "Create a new AiUserProfileEvaluationParameter", description = "Creates a new AiUserProfileEvaluationParameter record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameter created successfully",
            content = @Content(schema = @Schema(implementation = AiUserProfileEvaluationParameterOutputDTO.class))),
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
    public Mono<AiUserProfileEvaluationParameterOutputDTO> create(@Valid @RequestBody AiUserProfileEvaluationParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get AiUserProfileEvaluationParameter by ID
     */
    @Operation(summary = "Get AiUserProfileEvaluationParameter by ID", description = "Retrieves a AiUserProfileEvaluationParameter by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameter found",
            content = @Content(schema = @Schema(implementation = AiUserProfileEvaluationParameterOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiUserProfileEvaluationParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<AiUserProfileEvaluationParameterOutputDTO> findById(
            @Parameter(description = "AiUserProfileEvaluationParameter ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all AiUserProfileEvaluationParameter entities (paginated)
     */
    @Operation(summary = "Get all AiUserProfileEvaluationParameter entities (paginated)", description = "Retrieves AiUserProfileEvaluationParameter records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of AiUserProfileEvaluationParameter entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<AiUserProfileEvaluationParameterOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update AiUserProfileEvaluationParameter by ID
     */
    @Operation(summary = "Update AiUserProfileEvaluationParameter", description = "Updates an existing AiUserProfileEvaluationParameter by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameter updated successfully",
            content = @Content(schema = @Schema(implementation = AiUserProfileEvaluationParameterOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiUserProfileEvaluationParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<AiUserProfileEvaluationParameterOutputDTO> update(
            @Parameter(description = "AiUserProfileEvaluationParameter ID", required = true) @PathVariable Long id,
            @Valid @RequestBody AiUserProfileEvaluationParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete AiUserProfileEvaluationParameter by ID
     */
    @Operation(summary = "Delete AiUserProfileEvaluationParameter", description = "Deletes a AiUserProfileEvaluationParameter by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameter deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiUserProfileEvaluationParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "AiUserProfileEvaluationParameter ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete AiUserProfileEvaluationParameter with justification", description = "Deletes a AiUserProfileEvaluationParameter with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameter deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiUserProfileEvaluationParameter not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "AiUserProfileEvaluationParameter ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}