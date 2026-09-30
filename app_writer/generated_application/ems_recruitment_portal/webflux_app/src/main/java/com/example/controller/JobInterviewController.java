package com.example.controller;

import com.example.dto.JobInterviewInputDTO;
import com.example.dto.JobInterviewOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.JobInterviewService;
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
 * REST Controller for JobInterview endpoints.
 */
@RestController
@RequestMapping("/api/jobinterviews")
@RequiredArgsConstructor
@Tag(name = "JobInterview", description = "JobInterview management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class JobInterviewController {
    
    private final JobInterviewService service;
    
    /**
     * Create a new JobInterview
     */
    @Operation(summary = "Create a new JobInterview", description = "Creates a new JobInterview record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobInterview created successfully",
            content = @Content(schema = @Schema(implementation = JobInterviewOutputDTO.class))),
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
    public Mono<JobInterviewOutputDTO> create(@Valid @RequestBody JobInterviewInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get JobInterview by ID
     */
    @Operation(summary = "Get JobInterview by ID", description = "Retrieves a JobInterview by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobInterview found",
            content = @Content(schema = @Schema(implementation = JobInterviewOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobInterview not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<JobInterviewOutputDTO> findById(
            @Parameter(description = "JobInterview ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all JobInterview entities (paginated)
     */
    @Operation(summary = "Get all JobInterview entities (paginated)", description = "Retrieves JobInterview records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of JobInterview entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<JobInterviewOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update JobInterview by ID
     */
    @Operation(summary = "Update JobInterview", description = "Updates an existing JobInterview by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobInterview updated successfully",
            content = @Content(schema = @Schema(implementation = JobInterviewOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobInterview not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<JobInterviewOutputDTO> update(
            @Parameter(description = "JobInterview ID", required = true) @PathVariable Long id,
            @Valid @RequestBody JobInterviewInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete JobInterview by ID
     */
    @Operation(summary = "Delete JobInterview", description = "Deletes a JobInterview by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobInterview deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobInterview not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "JobInterview ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete JobInterview with justification", description = "Deletes a JobInterview with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobInterview deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobInterview not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "JobInterview ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}