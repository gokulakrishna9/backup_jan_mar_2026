package com.example.controller;

import com.example.dto.InstitutionAccreditationInputDTO;
import com.example.dto.InstitutionAccreditationOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.InstitutionAccreditationService;
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
 * REST Controller for InstitutionAccreditation endpoints.
 */
@RestController
@RequestMapping("/api/institutionaccreditations")
@RequiredArgsConstructor
@Tag(name = "InstitutionAccreditation", description = "InstitutionAccreditation management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class InstitutionAccreditationController {
    
    private final InstitutionAccreditationService service;
    
    /**
     * Create a new InstitutionAccreditation
     */
    @Operation(summary = "Create a new InstitutionAccreditation", description = "Creates a new InstitutionAccreditation record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "InstitutionAccreditation created successfully",
            content = @Content(schema = @Schema(implementation = InstitutionAccreditationOutputDTO.class))),
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
    public Mono<InstitutionAccreditationOutputDTO> create(@Valid @RequestBody InstitutionAccreditationInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get InstitutionAccreditation by ID
     */
    @Operation(summary = "Get InstitutionAccreditation by ID", description = "Retrieves a InstitutionAccreditation by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "InstitutionAccreditation found",
            content = @Content(schema = @Schema(implementation = InstitutionAccreditationOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "InstitutionAccreditation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<InstitutionAccreditationOutputDTO> findById(
            @Parameter(description = "InstitutionAccreditation ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all InstitutionAccreditation entities (paginated)
     */
    @Operation(summary = "Get all InstitutionAccreditation entities (paginated)", description = "Retrieves InstitutionAccreditation records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of InstitutionAccreditation entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<InstitutionAccreditationOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update InstitutionAccreditation by ID
     */
    @Operation(summary = "Update InstitutionAccreditation", description = "Updates an existing InstitutionAccreditation by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "InstitutionAccreditation updated successfully",
            content = @Content(schema = @Schema(implementation = InstitutionAccreditationOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "InstitutionAccreditation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<InstitutionAccreditationOutputDTO> update(
            @Parameter(description = "InstitutionAccreditation ID", required = true) @PathVariable Long id,
            @Valid @RequestBody InstitutionAccreditationInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete InstitutionAccreditation by ID
     */
    @Operation(summary = "Delete InstitutionAccreditation", description = "Deletes a InstitutionAccreditation by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "InstitutionAccreditation deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "InstitutionAccreditation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "InstitutionAccreditation ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete InstitutionAccreditation with justification", description = "Deletes a InstitutionAccreditation with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "InstitutionAccreditation deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "InstitutionAccreditation not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "InstitutionAccreditation ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}