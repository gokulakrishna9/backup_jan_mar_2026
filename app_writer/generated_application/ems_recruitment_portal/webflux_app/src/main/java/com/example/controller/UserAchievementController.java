package com.example.controller;

import com.example.dto.UserAchievementInputDTO;
import com.example.dto.UserAchievementOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.UserAchievementService;
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
 * REST Controller for UserAchievement endpoints.
 */
@RestController
@RequestMapping("/api/userachievements")
@RequiredArgsConstructor
@Tag(name = "UserAchievement", description = "UserAchievement management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class UserAchievementController {
    
    private final UserAchievementService service;
    
    /**
     * Create a new UserAchievement
     */
    @Operation(summary = "Create a new UserAchievement", description = "Creates a new UserAchievement record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserAchievement created successfully",
            content = @Content(schema = @Schema(implementation = UserAchievementOutputDTO.class))),
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
    public Mono<UserAchievementOutputDTO> create(@Valid @RequestBody UserAchievementInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get UserAchievement by ID
     */
    @Operation(summary = "Get UserAchievement by ID", description = "Retrieves a UserAchievement by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserAchievement found",
            content = @Content(schema = @Schema(implementation = UserAchievementOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserAchievement not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<UserAchievementOutputDTO> findById(
            @Parameter(description = "UserAchievement ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all UserAchievement entities (paginated)
     */
    @Operation(summary = "Get all UserAchievement entities (paginated)", description = "Retrieves UserAchievement records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of UserAchievement entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<UserAchievementOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update UserAchievement by ID
     */
    @Operation(summary = "Update UserAchievement", description = "Updates an existing UserAchievement by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserAchievement updated successfully",
            content = @Content(schema = @Schema(implementation = UserAchievementOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserAchievement not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<UserAchievementOutputDTO> update(
            @Parameter(description = "UserAchievement ID", required = true) @PathVariable Long id,
            @Valid @RequestBody UserAchievementInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete UserAchievement by ID
     */
    @Operation(summary = "Delete UserAchievement", description = "Deletes a UserAchievement by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserAchievement deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserAchievement not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "UserAchievement ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete UserAchievement with justification", description = "Deletes a UserAchievement with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserAchievement deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserAchievement not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "UserAchievement ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}