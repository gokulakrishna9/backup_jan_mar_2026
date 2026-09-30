package com.example.controller;

import com.example.dto.CommunityPropertyUserLinkInputDTO;
import com.example.dto.CommunityPropertyUserLinkOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.CommunityPropertyUserLinkService;
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
 * REST Controller for CommunityPropertyUserLink endpoints.
 */
@RestController
@RequestMapping("/api/communitypropertyuserlinks")
@RequiredArgsConstructor
@Tag(name = "CommunityPropertyUserLink", description = "CommunityPropertyUserLink management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class CommunityPropertyUserLinkController {
    
    private final CommunityPropertyUserLinkService service;
    
    /**
     * Create a new CommunityPropertyUserLink
     */
    @Operation(summary = "Create a new CommunityPropertyUserLink", description = "Creates a new CommunityPropertyUserLink record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyUserLink created successfully",
            content = @Content(schema = @Schema(implementation = CommunityPropertyUserLinkOutputDTO.class))),
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
    public Mono<CommunityPropertyUserLinkOutputDTO> create(@Valid @RequestBody CommunityPropertyUserLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get CommunityPropertyUserLink by ID
     */
    @Operation(summary = "Get CommunityPropertyUserLink by ID", description = "Retrieves a CommunityPropertyUserLink by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyUserLink found",
            content = @Content(schema = @Schema(implementation = CommunityPropertyUserLinkOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CommunityPropertyUserLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<CommunityPropertyUserLinkOutputDTO> findById(
            @Parameter(description = "CommunityPropertyUserLink ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all CommunityPropertyUserLink entities (paginated)
     */
    @Operation(summary = "Get all CommunityPropertyUserLink entities (paginated)", description = "Retrieves CommunityPropertyUserLink records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of CommunityPropertyUserLink entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<CommunityPropertyUserLinkOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update CommunityPropertyUserLink by ID
     */
    @Operation(summary = "Update CommunityPropertyUserLink", description = "Updates an existing CommunityPropertyUserLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyUserLink updated successfully",
            content = @Content(schema = @Schema(implementation = CommunityPropertyUserLinkOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CommunityPropertyUserLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<CommunityPropertyUserLinkOutputDTO> update(
            @Parameter(description = "CommunityPropertyUserLink ID", required = true) @PathVariable Long id,
            @Valid @RequestBody CommunityPropertyUserLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete CommunityPropertyUserLink by ID
     */
    @Operation(summary = "Delete CommunityPropertyUserLink", description = "Deletes a CommunityPropertyUserLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyUserLink deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CommunityPropertyUserLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "CommunityPropertyUserLink ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete CommunityPropertyUserLink with justification", description = "Deletes a CommunityPropertyUserLink with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CommunityPropertyUserLink deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CommunityPropertyUserLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "CommunityPropertyUserLink ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}