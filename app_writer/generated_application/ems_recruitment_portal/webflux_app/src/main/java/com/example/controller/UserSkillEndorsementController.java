package com.example.controller;

import com.example.dto.UserSkillEndorsementInputDTO;
import com.example.dto.UserSkillEndorsementOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.UserSkillEndorsementService;
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
 * REST Controller for UserSkillEndorsement endpoints.
 */
@RestController
@RequestMapping("/api/userskillendorsements")
@RequiredArgsConstructor
@Tag(name = "UserSkillEndorsement", description = "UserSkillEndorsement management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class UserSkillEndorsementController {
    
    private final UserSkillEndorsementService service;
    
    /**
     * Create a new UserSkillEndorsement
     */
    @Operation(summary = "Create a new UserSkillEndorsement", description = "Creates a new UserSkillEndorsement record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserSkillEndorsement created successfully",
            content = @Content(schema = @Schema(implementation = UserSkillEndorsementOutputDTO.class))),
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
    public Mono<UserSkillEndorsementOutputDTO> create(@Valid @RequestBody UserSkillEndorsementInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get UserSkillEndorsement by ID
     */
    @Operation(summary = "Get UserSkillEndorsement by ID", description = "Retrieves a UserSkillEndorsement by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserSkillEndorsement found",
            content = @Content(schema = @Schema(implementation = UserSkillEndorsementOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserSkillEndorsement not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<UserSkillEndorsementOutputDTO> findById(
            @Parameter(description = "UserSkillEndorsement ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all UserSkillEndorsement entities (paginated)
     */
    @Operation(summary = "Get all UserSkillEndorsement entities (paginated)", description = "Retrieves UserSkillEndorsement records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of UserSkillEndorsement entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<UserSkillEndorsementOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update UserSkillEndorsement by ID
     */
    @Operation(summary = "Update UserSkillEndorsement", description = "Updates an existing UserSkillEndorsement by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserSkillEndorsement updated successfully",
            content = @Content(schema = @Schema(implementation = UserSkillEndorsementOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserSkillEndorsement not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<UserSkillEndorsementOutputDTO> update(
            @Parameter(description = "UserSkillEndorsement ID", required = true) @PathVariable Long id,
            @Valid @RequestBody UserSkillEndorsementInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete UserSkillEndorsement by ID
     */
    @Operation(summary = "Delete UserSkillEndorsement", description = "Deletes a UserSkillEndorsement by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserSkillEndorsement deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserSkillEndorsement not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "UserSkillEndorsement ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete UserSkillEndorsement with justification", description = "Deletes a UserSkillEndorsement with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "UserSkillEndorsement deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "UserSkillEndorsement not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "UserSkillEndorsement ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}