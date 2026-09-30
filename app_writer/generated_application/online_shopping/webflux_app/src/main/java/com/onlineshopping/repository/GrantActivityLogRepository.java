package com.onlineshopping.repository;

import com.onlineshopping.entity.GrantActivityLog;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for GrantActivityLog entity.
 */
@Repository
public interface GrantActivityLogRepository extends ReactiveCrudRepository<GrantActivityLog, Long> {
    
    Flux<GrantActivityLog> findByTargetUserId(Long targetUserId);
    
    Flux<GrantActivityLog> findByGrantedByUserId(Long grantedByUserId);
    
    Flux<GrantActivityLog> findByGrantType(String grantType);
    
    @Query("SELECT * FROM grant_activity_log WHERE target_user_id = :userId ORDER BY timestamp DESC LIMIT :limit")
    Flux<GrantActivityLog> findRecentByTargetUserId(Long userId, int limit);
    
    @Query("SELECT * FROM grant_activity_log WHERE entity_type = :entityType AND entity_id = :entityId ORDER BY timestamp DESC")
    Flux<GrantActivityLog> findByEntityTypeAndEntityId(String entityType, Long entityId);
    
    @Query("SELECT * FROM grant_activity_log WHERE timestamp >= :startTime AND timestamp <= :endTime ORDER BY timestamp DESC")
    Flux<GrantActivityLog> findByTimestampBetween(java.time.LocalDateTime startTime, java.time.LocalDateTime endTime);
    
    @Query("SELECT * FROM grant_activity_log WHERE action = :action ORDER BY timestamp DESC LIMIT :limit")
    Flux<GrantActivityLog> findRecentByAction(String action, int limit);
}
