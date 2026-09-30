package com.example.repository;

import com.example.entity.CrudActivityLog;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for CrudActivityLog entity.
 */
@Repository
public interface CrudActivityLogRepository extends ReactiveCrudRepository<CrudActivityLog, Long> {
    
    Flux<CrudActivityLog> findByUserId(Long userId);
    
    Flux<CrudActivityLog> findByEntityTypeAndEntityId(String entityType, Long entityId);
    
    Flux<CrudActivityLog> findByOperation(String operation);
    
    @Query("SELECT * FROM crud_activity_log WHERE user_id = :userId AND operation = :operation ORDER BY timestamp DESC LIMIT :limit")
    Flux<CrudActivityLog> findRecentByUserIdAndOperation(Long userId, String operation, int limit);
    
    @Query("SELECT * FROM crud_activity_log WHERE entity_type = :entityType ORDER BY timestamp DESC LIMIT :limit")
    Flux<CrudActivityLog> findRecentByEntityType(String entityType, int limit);
    
    @Query("SELECT * FROM crud_activity_log WHERE timestamp >= :startTime AND timestamp <= :endTime ORDER BY timestamp DESC")
    Flux<CrudActivityLog> findByTimestampBetween(java.time.LocalDateTime startTime, java.time.LocalDateTime endTime);
}
