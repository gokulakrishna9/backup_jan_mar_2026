package com.example.controller;

import com.example.entity.*;
import com.example.service.ActivityTrackingService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * REST controller for querying activity tracking logs.
 * Provides endpoints for viewing CRUD, login, and grant activities.
 */
@RestController
@RequestMapping("/api/activity")
public class ActivityTrackingController {
    
    private final ActivityTrackingService activityTrackingService;
    
    public ActivityTrackingController(ActivityTrackingService activityTrackingService) {
        this.activityTrackingService = activityTrackingService;
    }
    
    /**
     * Get CRUD activity for a specific user.
     */
    @GetMapping("/crud/user/{userId}")
    public Flux<CrudActivityLog> getUserCrudActivity(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "100") int limit) {
        return activityTrackingService.getUserCrudActivity(userId, limit);
    }
    
    /**
     * Get complete history for a specific entity.
     */
    @GetMapping("/crud/entity/{entityType}/{entityId}")
    public Flux<CrudActivityLog> getEntityHistory(
            @PathVariable String entityType,
            @PathVariable Long entityId) {
        return activityTrackingService.getEntityHistory(entityType, entityId);
    }
    
    /**
     * Get login history for a specific user.
     */
    @GetMapping("/login/user/{userId}")
    public Flux<LoginActivityLog> getUserLoginHistory(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "50") int limit) {
        return activityTrackingService.getUserLoginHistory(userId, limit);
    }
    
    /**
     * Get grant/permission history for a specific user.
     */
    @GetMapping("/grant/user/{userId}")
    public Flux<GrantActivityLog> getUserGrantHistory(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "50") int limit) {
        return activityTrackingService.getUserGrantHistory(userId, limit);
    }
    
    /**
     * Get all restorable deleted records.
     */
    @GetMapping("/deleted")
    public Flux<DeletedRecord> getRestorableRecords(
            @RequestParam(required = false) String entityType) {
        return activityTrackingService.getRestorableRecords(entityType);
    }
    
    /**
     * Get a specific deleted record.
     */
    @GetMapping("/deleted/{entityType}/{entityId}")
    public Mono<ResponseEntity<DeletedRecord>> getDeletedRecord(
            @PathVariable String entityType,
            @PathVariable Long entityId) {
        return activityTrackingService.getDeletedRecord(entityType, entityId)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }
}
