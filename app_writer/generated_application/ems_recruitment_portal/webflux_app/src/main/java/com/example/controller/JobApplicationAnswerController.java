package com.example.controller;

import com.example.dto.JobApplicationAnswerInputDTO;
import com.example.dto.JobApplicationAnswerOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.JobApplicationAnswerService;
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
 * REST Controller for JobApplicationAnswer endpoints.
 */
@RestController
@RequestMapping("/api/jobapplicationanswers")
@RequiredArgsConstructor
@Tag(name = "JobApplicationAnswer", description = "JobApplicationAnswer management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class JobApplicationAnswerController {
    
    private final JobApplicationAnswerService service;
    
    /**
     * Create a new JobApplicationAnswer
     */
    @Operation(summary = "Create a new JobApplicationAnswer", description = "Creates a new JobApplicationAnswer record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobApplicationAnswer created successfully",
            content = @Content(schema = @Schema(implementation = JobApplicationAnswerOutputDTO.class))),
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
    public Mono<JobApplicationAnswerOutputDTO> create(@Valid @RequestBody JobApplicationAnswerInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get JobApplicationAnswer by ID
     */
    @Operation(summary = "Get JobApplicationAnswer by ID", description = "Retrieves a JobApplicationAnswer by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobApplicationAnswer found",
            content = @Content(schema = @Schema(implementation = JobApplicationAnswerOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobApplicationAnswer not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<JobApplicationAnswerOutputDTO> findById(
            @Parameter(description = "JobApplicationAnswer ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all JobApplicationAnswer entities (paginated)
     */
    @Operation(summary = "Get all JobApplicationAnswer entities (paginated)", description = "Retrieves JobApplicationAnswer records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of JobApplicationAnswer entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<JobApplicationAnswerOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update JobApplicationAnswer by ID
     */
    @Operation(summary = "Update JobApplicationAnswer", description = "Updates an existing JobApplicationAnswer by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobApplicationAnswer updated successfully",
            content = @Content(schema = @Schema(implementation = JobApplicationAnswerOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobApplicationAnswer not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<JobApplicationAnswerOutputDTO> update(
            @Parameter(description = "JobApplicationAnswer ID", required = true) @PathVariable Long id,
            @Valid @RequestBody JobApplicationAnswerInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete JobApplicationAnswer by ID
     */
    @Operation(summary = "Delete JobApplicationAnswer", description = "Deletes a JobApplicationAnswer by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobApplicationAnswer deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobApplicationAnswer not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "JobApplicationAnswer ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete JobApplicationAnswer with justification", description = "Deletes a JobApplicationAnswer with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "JobApplicationAnswer deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "JobApplicationAnswer not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "JobApplicationAnswer ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}