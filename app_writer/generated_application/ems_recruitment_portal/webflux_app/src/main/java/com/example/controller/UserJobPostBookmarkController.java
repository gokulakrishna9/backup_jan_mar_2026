package com.example.controller;

import com.example.dto.UserJobPostBookmarkInputDTO;
import com.example.dto.UserJobPostBookmarkOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.UserJobPostBookmarkService;
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
 * REST Controller for UserJobPostBookmark endpoints.
 */
@RestController
@RequestMapping("/api/userjobpostbookmarks")
@RequiredArgsConstructor
@Tag(name = "UserJobPostBookmark", description = "UserJobPostBookmark management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class UserJobPostBookmarkController {
    
    private final UserJobPostBookmarkService service;
    
    /**
     * Create a new UserJobPostBookmark
     */
    @Operation(summary = "Create a new UserJobPostBookmark", description = "Creates a new UserJobPostBookmark record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserJobPostBookmark created successfully",
            content = @Content(schema = @Schema(implementation = UserJobPostBookmarkOutputDTO.class))),
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
    public Mono<UserJobPostBookmarkOutputDTO> create(@Valid @RequestBody UserJobPostBookmarkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get UserJobPostBookmark by ID
     */
    @Operation(summary = "Get UserJobPostBookmark by ID", description = "Retrieves a UserJobPostBookmark by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserJobPostBookmark found",
            content = @Content(schema = @Schema(implementation = UserJobPostBookmarkOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserJobPostBookmark not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<UserJobPostBookmarkOutputDTO> findById(
            @Parameter(description = "UserJobPostBookmark ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all UserJobPostBookmark entities (paginated)
     */
    @Operation(summary = "Get all UserJobPostBookmark entities (paginated)", description = "Retrieves UserJobPostBookmark records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of UserJobPostBookmark entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<UserJobPostBookmarkOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update UserJobPostBookmark by ID
     */
    @Operation(summary = "Update UserJobPostBookmark", description = "Updates an existing UserJobPostBookmark by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserJobPostBookmark updated successfully",
            content = @Content(schema = @Schema(implementation = UserJobPostBookmarkOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserJobPostBookmark not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<UserJobPostBookmarkOutputDTO> update(
            @Parameter(description = "UserJobPostBookmark ID", required = true) @PathVariable Long id,
            @Valid @RequestBody UserJobPostBookmarkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete UserJobPostBookmark by ID
     */
    @Operation(summary = "Delete UserJobPostBookmark", description = "Deletes a UserJobPostBookmark by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserJobPostBookmark deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserJobPostBookmark not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "UserJobPostBookmark ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete UserJobPostBookmark with justification", description = "Deletes a UserJobPostBookmark with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserJobPostBookmark deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserJobPostBookmark not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "UserJobPostBookmark ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}