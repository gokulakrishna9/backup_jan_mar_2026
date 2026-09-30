package com.example.repository;

import com.example.entity.RecordOwner;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface RecordOwnerRepository extends R2dbcRepository<RecordOwner, Long> {
    
    Flux<RecordOwner> findByAuthUserIdAndTableName(Long authUserId, String tableName);
    Flux<RecordOwner> findByTableNameAndRecordId(String tableName, Long recordId);
    Mono<Void> deleteByTableNameAndRecordId(String tableName, Long recordId);
    Mono<Boolean> existsByAuthUserIdAndTableNameAndRecordId(Long authUserId, String tableName, Long recordId);
}