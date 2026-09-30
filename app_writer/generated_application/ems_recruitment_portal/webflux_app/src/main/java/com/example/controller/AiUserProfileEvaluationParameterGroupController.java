package com.example.controller;

import com.example.dto.AiUserProfileEvaluationParameterGroupInputDTO;
import com.example.dto.AiUserProfileEvaluationParameterGroupOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.AiUserProfileEvaluationParameterGroupService;
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
 * REST Controller for AiUserProfileEvaluationParameterGroup endpoints.
 */
@RestController
@RequestMapping("/api/aiuserprofileevaluationparametergroups")
@RequiredArgsConstructor
@Tag(name = "AiUserProfileEvaluationParameterGroup", description = "AiUserProfileEvaluationParameterGroup management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class AiUserProfileEvaluationParameterGroupController {
    
    private final AiUserProfileEvaluationParameterGroupService service;
    
    /**
     * Create a new AiUserProfileEvaluationParameterGroup
     */
    @Operation(summary = "Create a new AiUserProfileEvaluationParameterGroup", description = "Creates a new AiUserProfileEvaluationParameterGroup record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameterGroup created successfully",
            content = @Content(schema = @Schema(implementation = AiUserProfileEvaluationParameterGroupOutputDTO.class))),
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
    public Mono<AiUserProfileEvaluationParameterGroupOutputDTO> create(@Valid @RequestBody AiUserProfileEvaluationParameterGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get AiUserProfileEvaluationParameterGroup by ID
     */
    @Operation(summary = "Get AiUserProfileEvaluationParameterGroup by ID", description = "Retrieves a AiUserProfileEvaluationParameterGroup by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameterGroup found",
            content = @Content(schema = @Schema(implementation = AiUserProfileEvaluationParameterGroupOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiUserProfileEvaluationParameterGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<AiUserProfileEvaluationParameterGroupOutputDTO> findById(
            @Parameter(description = "AiUserProfileEvaluationParameterGroup ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all AiUserProfileEvaluationParameterGroup entities (paginated)
     */
    @Operation(summary = "Get all AiUserProfileEvaluationParameterGroup entities (paginated)", description = "Retrieves AiUserProfileEvaluationParameterGroup records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of AiUserProfileEvaluationParameterGroup entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<AiUserProfileEvaluationParameterGroupOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update AiUserProfileEvaluationParameterGroup by ID
     */
    @Operation(summary = "Update AiUserProfileEvaluationParameterGroup", description = "Updates an existing AiUserProfileEvaluationParameterGroup by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameterGroup updated successfully",
            content = @Content(schema = @Schema(implementation = AiUserProfileEvaluationParameterGroupOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiUserProfileEvaluationParameterGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<AiUserProfileEvaluationParameterGroupOutputDTO> update(
            @Parameter(description = "AiUserProfileEvaluationParameterGroup ID", required = true) @PathVariable Long id,
            @Valid @RequestBody AiUserProfileEvaluationParameterGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete AiUserProfileEvaluationParameterGroup by ID
     */
    @Operation(summary = "Delete AiUserProfileEvaluationParameterGroup", description = "Deletes a AiUserProfileEvaluationParameterGroup by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameterGroup deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiUserProfileEvaluationParameterGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "AiUserProfileEvaluationParameterGroup ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete AiUserProfileEvaluationParameterGroup with justification", description = "Deletes a AiUserProfileEvaluationParameterGroup with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "AiUserProfileEvaluationParameterGroup deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "AiUserProfileEvaluationParameterGroup not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "AiUserProfileEvaluationParameterGroup ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}