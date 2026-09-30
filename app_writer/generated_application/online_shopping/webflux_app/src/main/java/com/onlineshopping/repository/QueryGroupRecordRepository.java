package com.onlineshopping.repository;

import com.onlineshopping.entity.QueryGroupRecord;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface QueryGroupRecordRepository extends R2dbcRepository<QueryGroupRecord, Long> {
    
    Flux<QueryGroupRecord> findByQueryGroupId(Long queryGroupId);
    Flux<QueryGroupRecord> findByTableNameAndRecordId(String tableName, Long recordId);
    Mono<Boolean> existsByQueryGroupIdAndTableNameAndRecordId(Long queryGroupId, String tableName, Long recordId);
}