package com.jobportal.repository;

import com.jobportal.entity.RecordOwner;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface RecordOwnerRepository extends R2dbcRepository<RecordOwner, Long> {
    
    Flux<RecordOwner> findByAuthUserIdAndTableName(Long authUserId, String tableName);
    Flux<RecordOwner> findByTableNameAndRecordId(String tableName, Long recordId);
    @org.springframework.data.r2dbc.repository.Query("DELETE FROM record_owner WHERE table_name = :tableName AND record_id = :recordId")
    Mono<Void> deleteByTableNameAndRecordId(String tableName, Long recordId);
    Mono<Boolean> existsByAuthUserIdAndTableNameAndRecordId(Long authUserId, String tableName, Long recordId);
}