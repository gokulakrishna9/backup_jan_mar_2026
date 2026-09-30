package com.onlineshopping.repository;

import com.onlineshopping.entity.QueryGroup;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface QueryGroupRepository extends R2dbcRepository<QueryGroup, Long> {
    
    Flux<QueryGroup> findByGroupType(String groupType);
    Flux<QueryGroup> findByOwnerAuthUserId(Long ownerAuthUserId);
    Mono<QueryGroup> findByGroupName(String groupName);
}