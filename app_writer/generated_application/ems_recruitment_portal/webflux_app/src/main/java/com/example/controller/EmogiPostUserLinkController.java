package com.example.controller;

import com.example.dto.EmogiPostUserLinkInputDTO;
import com.example.dto.EmogiPostUserLinkOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.EmogiPostUserLinkService;
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
 * REST Controller for EmogiPostUserLink endpoints.
 */
@RestController
@RequestMapping("/api/emogipostuserlinks")
@RequiredArgsConstructor
@Tag(name = "EmogiPostUserLink", description = "EmogiPostUserLink management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class EmogiPostUserLinkController {
    
    private final EmogiPostUserLinkService service;
    
    /**
     * Create a new EmogiPostUserLink
     */
    @Operation(summary = "Create a new EmogiPostUserLink", description = "Creates a new EmogiPostUserLink record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "EmogiPostUserLink created successfully",
            content = @Content(schema = @Schema(implementation = EmogiPostUserLinkOutputDTO.class))),
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
    public Mono<EmogiPostUserLinkOutputDTO> create(@Valid @RequestBody EmogiPostUserLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get EmogiPostUserLink by ID
     */
    @Operation(summary = "Get EmogiPostUserLink by ID", description = "Retrieves a EmogiPostUserLink by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "EmogiPostUserLink found",
            content = @Content(schema = @Schema(implementation = EmogiPostUserLinkOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "EmogiPostUserLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<EmogiPostUserLinkOutputDTO> findById(
            @Parameter(description = "EmogiPostUserLink ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all EmogiPostUserLink entities (paginated)
     */
    @Operation(summary = "Get all EmogiPostUserLink entities (paginated)", description = "Retrieves EmogiPostUserLink records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of EmogiPostUserLink entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<EmogiPostUserLinkOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update EmogiPostUserLink by ID
     */
    @Operation(summary = "Update EmogiPostUserLink", description = "Updates an existing EmogiPostUserLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "EmogiPostUserLink updated successfully",
            content = @Content(schema = @Schema(implementation = EmogiPostUserLinkOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "EmogiPostUserLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<EmogiPostUserLinkOutputDTO> update(
            @Parameter(description = "EmogiPostUserLink ID", required = true) @PathVariable Long id,
            @Valid @RequestBody EmogiPostUserLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete EmogiPostUserLink by ID
     */
    @Operation(summary = "Delete EmogiPostUserLink", description = "Deletes a EmogiPostUserLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "EmogiPostUserLink deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "EmogiPostUserLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "EmogiPostUserLink ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete EmogiPostUserLink with justification", description = "Deletes a EmogiPostUserLink with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "EmogiPostUserLink deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "EmogiPostUserLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "EmogiPostUserLink ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}