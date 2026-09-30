package com.jobportal.controller;

import com.jobportal.dto.CourseVideoInputDTO;
import com.jobportal.dto.CourseVideoOutputDTO;
import com.jobportal.dto.PageResponse;
import com.jobportal.service.CourseVideoService;
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
 * REST Controller for CourseVideo endpoints.
 */
@RestController
@RequestMapping("/api/course_videos")
@RequiredArgsConstructor
@Tag(name = "CourseVideo", description = "CourseVideo management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class CourseVideoController {
    
    private final CourseVideoService service;
    
    /**
     * Create a new CourseVideo
     */
    @Operation(summary = "Create a new CourseVideo", description = "Creates a new CourseVideo record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CourseVideo created successfully",
            content = @Content(schema = @Schema(implementation = CourseVideoOutputDTO.class))),
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
    public Mono<CourseVideoOutputDTO> create(@Valid @RequestBody CourseVideoInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get CourseVideo by ID
     */
    @Operation(summary = "Get CourseVideo by ID", description = "Retrieves a CourseVideo by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CourseVideo found",
            content = @Content(schema = @Schema(implementation = CourseVideoOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CourseVideo not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<CourseVideoOutputDTO> findById(
            @Parameter(description = "CourseVideo ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all CourseVideo entities (paginated)
     */
    @Operation(summary = "Get all CourseVideo entities (paginated)", description = "Retrieves CourseVideo records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of CourseVideo entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<CourseVideoOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update CourseVideo by ID
     */
    @Operation(summary = "Update CourseVideo", description = "Updates an existing CourseVideo by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CourseVideo updated successfully",
            content = @Content(schema = @Schema(implementation = CourseVideoOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CourseVideo not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<CourseVideoOutputDTO> update(
            @Parameter(description = "CourseVideo ID", required = true) @PathVariable Long id,
            @Valid @RequestBody CourseVideoInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete CourseVideo by ID
     */
    @Operation(summary = "Delete CourseVideo", description = "Deletes a CourseVideo by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CourseVideo deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CourseVideo not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(
            @Parameter(description = "CourseVideo ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete CourseVideo with justification", description = "Deletes a CourseVideo with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CourseVideo deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CourseVideo not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "CourseVideo ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}