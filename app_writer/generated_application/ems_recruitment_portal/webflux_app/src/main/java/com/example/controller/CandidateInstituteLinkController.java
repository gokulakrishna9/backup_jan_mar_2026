package com.example.controller;

import com.example.dto.CandidateInstituteLinkInputDTO;
import com.example.dto.CandidateInstituteLinkOutputDTO;
import com.example.dto.PageResponse;
import com.example.service.CandidateInstituteLinkService;
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
 * REST Controller for CandidateInstituteLink endpoints.
 */
@RestController
@RequestMapping("/api/candidateinstitutelinks")
@RequiredArgsConstructor
@Tag(name = "CandidateInstituteLink", description = "CandidateInstituteLink management APIs")
@EntityTable("")
@CrossOrigin(
    origins = { "*" },
    methods = { RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE },
    allowedHeaders = { "*" },
    maxAge = 3600
)
public class CandidateInstituteLinkController {
    
    private final CandidateInstituteLinkService service;
    
    /**
     * Create a new CandidateInstituteLink
     */
    @Operation(summary = "Create a new CandidateInstituteLink", description = "Creates a new CandidateInstituteLink record")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CandidateInstituteLink created successfully",
            content = @Content(schema = @Schema(implementation = CandidateInstituteLinkOutputDTO.class))),
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
    public Mono<CandidateInstituteLinkOutputDTO> create(@Valid @RequestBody CandidateInstituteLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.create(inputDTO, exchange);
    }
    
    /**
     * Get CandidateInstituteLink by ID
     */
    @Operation(summary = "Get CandidateInstituteLink by ID", description = "Retrieves a CandidateInstituteLink by its unique identifier")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CandidateInstituteLink found",
            content = @Content(schema = @Schema(implementation = CandidateInstituteLinkOutputDTO.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CandidateInstituteLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("/{id}")
    public Mono<CandidateInstituteLinkOutputDTO> findById(
            @Parameter(description = "CandidateInstituteLink ID", required = true) @PathVariable Long id) {
        return service.findById(id);
    }
    
    /**
     * Get all CandidateInstituteLink entities (paginated)
     */
    @Operation(summary = "Get all CandidateInstituteLink entities (paginated)", description = "Retrieves CandidateInstituteLink records with pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Paginated list of CandidateInstituteLink entities"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "READ")
    @GetMapping("")
    public Mono<PageResponse<CandidateInstituteLinkOutputDTO>> findAll(
            @Parameter(description = "Page number (zero-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "20") int size) {
        return service.findAllPaged(page, size);
    }
    
    /**
     * Update CandidateInstituteLink by ID
     */
    @Operation(summary = "Update CandidateInstituteLink", description = "Updates an existing CandidateInstituteLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CandidateInstituteLink updated successfully",
            content = @Content(schema = @Schema(implementation = CandidateInstituteLinkOutputDTO.class))),
        @ApiResponse(responseCode = "400", description = "Validation error - invalid input data",
            content = @Content(schema = @Schema(implementation = ValidationErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CandidateInstituteLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "UPDATE")
    @PutMapping("/{id}")
    public Mono<CandidateInstituteLinkOutputDTO> update(
            @Parameter(description = "CandidateInstituteLink ID", required = true) @PathVariable Long id,
            @Valid @RequestBody CandidateInstituteLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return service.update(id, inputDTO, exchange);
    }
    
    /**
     * Delete CandidateInstituteLink by ID
     */
    @Operation(summary = "Delete CandidateInstituteLink", description = "Deletes a CandidateInstituteLink by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CandidateInstituteLink deleted successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CandidateInstituteLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}")
    public Mono<Void> delete(
            @Parameter(description = "CandidateInstituteLink ID", required = true) @PathVariable Long id, ServerWebExchange exchange) {
        return service.delete(id, exchange);
    }
    
    /**
     * Delete with justification (for super users performing DELETE operations)
     */
    @Operation(summary = "Delete CandidateInstituteLink with justification", description = "Deletes a CandidateInstituteLink with a required justification (for audit purposes)")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "CandidateInstituteLink deleted successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - justification required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "401", description = "Unauthorized - authentication required",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "403", description = "Forbidden - insufficient permissions",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "404", description = "CandidateInstituteLink not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @TableAccess(operation = "DELETE")
    @DeleteMapping("/{id}/with-justification")
    public Mono<Void> deleteWithJustification(
            @Parameter(description = "CandidateInstituteLink ID", required = true) @PathVariable Long id, 
            @Parameter(description = "Justification for deletion", required = true) @RequestParam String justification,
            ServerWebExchange exchange) {
        return service.deleteWithJustification(id, justification, exchange);
    }
}