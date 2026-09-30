package com.jobportal.controller;

import com.jobportal.dto.UserProfileInputDTO;
import com.jobportal.dto.UserProfileOutputDTO;
import com.jobportal.dto.PageResponse;
import com.jobportal.service.UserProfileService;
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
 * REST Controller for UserProfile endpoints.
 */
@RestController
@RequestMapping("/api/user_profiles")
@RequiredArgsConstructor
@Tag(name = "UserProfile", description = "UserProfile management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class UserProfileController {
    
    private final UserProfileService service;
    
    /**
     * Create a new UserProfile
     */
    @Operation(summary = "Create a new UserProfile", description = "Creates a new UserProfile record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserProfile created successfully",
            content = @Content(schema = @Schema(implementation = UserProfileOutputDTO.class))),
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
    public Mono<UserProfileOutputDTO> create(@Valid @RequestBody UserProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get UserProfile by ID
     */
    @Operation(summary = "Get UserProfile by ID", description = "Retrieves a UserProfile by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserProfile found",
            content = @Content(schema = @Schema(implementation = UserProfileOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserProfile not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<UserProfileOutputDTO> findById(
            @Parameter(description = "UserProfile ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all UserProfile entities (paginated)
     */
    @Operation(summary = "Get all UserProfile entities (paginated)", description = "Retrieves UserProfile records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of UserProfile entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<UserProfileOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update UserProfile by ID
     */
    @Operation(summary = "Update UserProfile", description = "Updates an existing UserProfile by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserProfile updated successfully",
            content = @Content(schema = @Schema(implementation = UserProfileOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserProfile not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<UserProfileOutputDTO> update(
            @Parameter(description = "UserProfile ID", required = true) @PathVariable Long id,
            @Valid @RequestBody UserProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete UserProfile by ID
     */
    @Operation(summary = "Delete UserProfile", description = "Deletes a UserProfile by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserProfile deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserProfile not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(
            @Parameter(description = "UserProfile ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete UserProfile with justification", description = "Deletes a UserProfile with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserProfile deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserProfile not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "UserProfile ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
    
    /**
     * Get the current user's own UserProfile record (single-record-per-user)
     */
    @Operation(summary = "Get my UserProfile", description = "Retrieves the current authenticated user's own UserProfile record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserProfile found",
            content = @Content(schema = @Schema(implementation = UserProfileOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "No UserProfile record found for current user",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/me")
    public Mono<UserProfileOutputDTO> findMyRecord() {
        return service.findMyRecord();
    }
}