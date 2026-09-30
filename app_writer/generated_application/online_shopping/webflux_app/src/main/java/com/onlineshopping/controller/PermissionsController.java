package com.onlineshopping.controller;

import com.onlineshopping.service.PermissionsService;
import com.onlineshopping.security.SecurityContextHolder;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import java.util.List;

/**
 * Exposes the authenticated user's allowed API operations.
 * The React frontend calls this after login to populate allowedApiList
 * in AuthContext, which drives usePermissions visibility checks.
 */
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@Tag(name = "Permissions", description = "User permission resolution APIs")
public class PermissionsController {

    private final PermissionsService permissionsService;

    @Operation(
        summary = "Get current user's allowed API operations",
        description = "Returns a list of HTTP method + path pairs the authenticated user is permitted to call, "
                    + "resolved from user roles and table assignments."
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Permissions resolved successfully"),
        @ApiResponse(responseCode = "401", description = "Unauthorized — authentication required")
    })
    @GetMapping("/permissions")
    public Mono<List<PermissionsService.AllowedApi>> getPermissions() {
        return SecurityContextHolder.getCurrentUserId()
            .flatMap(permissionsService::resolveAllowedApis);
    }
}