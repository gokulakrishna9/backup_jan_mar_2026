package com.example.controller;

import com.example.dto.JobPostUserBookmarkInputDTO;
import com.example.dto.JobPostUserBookmarkOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.JobPostUserBookmarkService;
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
 * REST Controller for JobPostUserBookmark endpoints.
 */
@RestController
@RequestMapping("/api/jobpostuserbookmarks")
@RequiredArgsConstructor
@Tag(name = "JobPostUserBookmark", description = "JobPostUserBookmark management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class JobPostUserBookmarkController {
    
    private final JobPostUserBookmarkService service;
    
    /**
     * Create a new JobPostUserBookmark
     */
    @Operation(summary = "Create a new JobPostUserBookmark", description = "Creates a new JobPostUserBookmark record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobPostUserBookmark created successfully",
            content = @Content(schema = @Schema(implementation = JobPostUserBookmarkOutputDTO.class))),
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
    public Mono<JobPostUserBookmarkOutputDTO> create(@Valid @RequestBody JobPostUserBookmarkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get JobPostUserBookmark by ID
     */
    @Operation(summary = "Get JobPostUserBookmark by ID", description = "Retrieves a JobPostUserBookmark by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobPostUserBookmark found",
            content = @Content(schema = @Schema(implementation = JobPostUserBookmarkOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobPostUserBookmark not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<JobPostUserBookmarkOutputDTO> findById(
            @Parameter(description = "JobPostUserBookmark ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all JobPostUserBookmark entities (paginated)
     */
    @Operation(summary = "Get all JobPostUserBookmark entities (paginated)", description = "Retrieves JobPostUserBookmark records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of JobPostUserBookmark entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<JobPostUserBookmarkOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update JobPostUserBookmark by ID
     */
    @Operation(summary = "Update JobPostUserBookmark", description = "Updates an existing JobPostUserBookmark by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobPostUserBookmark updated successfully",
            content = @Content(schema = @Schema(implementation = JobPostUserBookmarkOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobPostUserBookmark not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<JobPostUserBookmarkOutputDTO> update(
            @Parameter(description = "JobPostUserBookmark ID", required = true) @PathVariable Long id,
            @Valid @RequestBody JobPostUserBookmarkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete JobPostUserBookmark by ID
     */
    @Operation(summary = "Delete JobPostUserBookmark", description = "Deletes a JobPostUserBookmark by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobPostUserBookmark deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobPostUserBookmark not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "JobPostUserBookmark ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete JobPostUserBookmark with justification", description = "Deletes a JobPostUserBookmark with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobPostUserBookmark deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobPostUserBookmark not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "JobPostUserBookmark ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}