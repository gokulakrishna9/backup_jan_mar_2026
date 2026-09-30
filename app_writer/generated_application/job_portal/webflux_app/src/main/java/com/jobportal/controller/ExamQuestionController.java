package com.jobportal.controller;

import com.jobportal.dto.ExamQuestionInputDTO;
import com.jobportal.dto.ExamQuestionOutputDTO;
import com.jobportal.dto.PageResponse;
import com.jobportal.service.ExamQuestionService;
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
 * REST Controller for ExamQuestion endpoints.
 */
@RestController
@RequestMapping("/api/exam_questions")
@RequiredArgsConstructor
@Tag(name = "ExamQuestion", description = "ExamQuestion management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class ExamQuestionController {
    
    private final ExamQuestionService service;
    
    /**
     * Create a new ExamQuestion
     */
    @Operation(summary = "Create a new ExamQuestion", description = "Creates a new ExamQuestion record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamQuestion created successfully",
            content = @Content(schema = @Schema(implementation = ExamQuestionOutputDTO.class))),
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
    public Mono<ExamQuestionOutputDTO> create(@Valid @RequestBody ExamQuestionInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get ExamQuestion by ID
     */
    @Operation(summary = "Get ExamQuestion by ID", description = "Retrieves a ExamQuestion by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamQuestion found",
            content = @Content(schema = @Schema(implementation = ExamQuestionOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ExamQuestion not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<ExamQuestionOutputDTO> findById(
            @Parameter(description = "ExamQuestion ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all ExamQuestion entities (paginated)
     */
    @Operation(summary = "Get all ExamQuestion entities (paginated)", description = "Retrieves ExamQuestion records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of ExamQuestion entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<ExamQuestionOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update ExamQuestion by ID
     */
    @Operation(summary = "Update ExamQuestion", description = "Updates an existing ExamQuestion by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamQuestion updated successfully",
            content = @Content(schema = @Schema(implementation = ExamQuestionOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ExamQuestion not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<ExamQuestionOutputDTO> update(
            @Parameter(description = "ExamQuestion ID", required = true) @PathVariable Long id,
            @Valid @RequestBody ExamQuestionInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete ExamQuestion by ID
     */
    @Operation(summary = "Delete ExamQuestion", description = "Deletes a ExamQuestion by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamQuestion deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ExamQuestion not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(
            @Parameter(description = "ExamQuestion ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete ExamQuestion with justification", description = "Deletes a ExamQuestion with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "ExamQuestion deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "ExamQuestion not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "ExamQuestion ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}