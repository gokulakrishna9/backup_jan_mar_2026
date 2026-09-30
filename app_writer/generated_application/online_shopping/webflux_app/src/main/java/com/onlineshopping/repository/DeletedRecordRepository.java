package com.onlineshopping.repository;

import com.onlineshopping.entity.DeletedRecord;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for DeletedRecord entity.
 */
@Repository
public interface DeletedRecordRepository extends ReactiveCrudRepository<DeletedRecord, Long> {
    
    Flux<DeletedRecord> findByEntityType(String entityType);
    
    Mono<DeletedRecord> findByEntityTypeAndEntityId(String entityType, Long entityId);
    
    Flux<DeletedRecord> findByDeletedByUserId(Long deletedByUserId);
    
    @Query("SELECT * FROM deleted_record WHERE can_restore = true ORDER BY deleted_at DESC")
    Flux<DeletedRecord> findAllRestorableRecords();
    
    @Query("SELECT * FROM deleted_record WHERE entity_type = :entityType AND can_restore = true ORDER BY deleted_at DESC")
    Flux<DeletedRecord> findRestorableByEntityType(String entityType);
    
    @Query("SELECT * FROM deleted_record WHERE deleted_at >= :startTime AND deleted_at <= :endTime ORDER BY deleted_at DESC")
    Flux<DeletedRecord> findByDeletedAtBetween(java.time.LocalDateTime startTime, java.time.LocalDateTime endTime);
}
