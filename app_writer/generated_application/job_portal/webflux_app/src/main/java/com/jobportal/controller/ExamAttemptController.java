package com.jobportal.controller;

import com.jobportal.dto.ExamAttemptInputDTO;
import com.jobportal.dto.ExamAttemptOutputDTO;
import com.jobportal.dto.PageResponse;
import com.jobportal.service.ExamAttemptService;
import com.jobportal.exception.ErrorResponse;
import com.jobportal.exception.ValidationErrorResponse;
import com.jobportal.security.EntityTable;
import com.jobportal.security.TableAccess;
import com.jobportal.security.QueryAccess;
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
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import jakarta.validation.Valid;

/**
 * REST Controller for ExamAttempt endpoints.
 */
@RestController
@RequestMapping("/api/exam_attempts")
@RequiredArgsConstructor
@Tag(name = "ExamAttempt", description = "ExamAttempt management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class ExamAttemptController {
    
    private final ExamAttemptService service;
    
    /**
     * Create a new ExamAttempt
     */
    @Operation(summary = "Create a new ExamAttempt", description = "Creates a new ExamAttempt record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamAttempt created successfully",
            content = @Content(schema = @Schema(implementation = ExamAttemptOutputDTO.class))),
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
    public Mono<ExamAttemptOutputDTO> create(@Valid @RequestBody ExamAttemptInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get ExamAttempt by ID
     */
    @Operation(summary = "Get ExamAttempt by ID", description = "Retrieves a ExamAttempt by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamAttempt found",
            content = @Content(schema = @Schema(implementation = ExamAttemptOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ExamAttempt not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<ExamAttemptOutputDTO> findById(
            @Parameter(description = "ExamAttempt ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all ExamAttempt entities (paginated)
     */
    @Operation(summary = "Get all ExamAttempt entities (paginated)", description = "Retrieves ExamAttempt records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of ExamAttempt entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<ExamAttemptOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update ExamAttempt by ID
     */
    @Operation(summary = "Update ExamAttempt", description = "Updates an existing ExamAttempt by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamAttempt updated successfully",
            content = @Content(schema = @Schema(implementation = ExamAttemptOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ExamAttempt not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<ExamAttemptOutputDTO> update(
            @Parameter(description = "ExamAttempt ID", required = true) @PathVariable Long id,
            @Valid @RequestBody ExamAttemptInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete ExamAttempt by ID
     */
    @Operation(summary = "Delete ExamAttempt", description = "Deletes a ExamAttempt by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamAttempt deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ExamAttempt not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(
            @Parameter(description = "ExamAttempt ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete ExamAttempt with justification", description = "Deletes a ExamAttempt with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamAttempt deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ExamAttempt not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "ExamAttempt ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}