package com.example.repository;

import com.example.entity.LoginActivityLog;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for LoginActivityLog entity.
 */
@Repository
public interface LoginActivityLogRepository extends ReactiveCrudRepository<LoginActivityLog, Long> {
    
    Flux<LoginActivityLog> findByUserId(Long userId);
    
    Flux<LoginActivityLog> findByActivityType(String activityType);
    
    Flux<LoginActivityLog> findByUsername(String username);
    
    @Query("SELECT * FROM login_activity_log WHERE user_id = :userId ORDER BY timestamp DESC LIMIT :limit")
    Flux<LoginActivityLog> findRecentByUserId(Long userId, int limit);
    
    @Query("SELECT * FROM login_activity_log WHERE success = false ORDER BY timestamp DESC LIMIT :limit")
    Flux<LoginActivityLog> findRecentFailedLogins(int limit);
    
    @Query("SELECT * FROM login_activity_log WHERE username = :username AND success = false AND timestamp >= :since")
    Flux<LoginActivityLog> findFailedLoginsSince(String username, java.time.LocalDateTime since);
    
    @Query("SELECT * FROM login_activity_log WHERE timestamp >= :startTime AND timestamp <= :endTime ORDER BY timestamp DESC")
    Flux<LoginActivityLog> findByTimestampBetween(java.time.LocalDateTime startTime, java.time.LocalDateTime endTime);
    
    @Query("SELECT * FROM login_activity_log WHERE activity_type = 'LOGIN' AND success = true AND user_id = :userId ORDER BY timestamp DESC LIMIT 1")
    Mono<LoginActivityLog> findLastSuccessfulLogin(Long userId);
}
