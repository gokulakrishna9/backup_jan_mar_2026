package com.onlineshopping.repository;

import com.onlineshopping.entity.QueryGroupMember;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface QueryGroupMemberRepository extends R2dbcRepository<QueryGroupMember, Long> {
    
    Flux<QueryGroupMember> findByQueryGroupId(Long queryGroupId);
    Flux<QueryGroupMember> findByAuthUserId(Long authUserId);
    Mono<Boolean> existsByQueryGroupIdAndAuthUserId(Long queryGroupId, Long authUserId);
}