package com.onlineshopping.repository;

import com.onlineshopping.entity.QueryGroupQuery;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

@Repository
public interface QueryGroupQueryRepository extends R2dbcRepository<QueryGroupQuery, Long> {
    
    Flux<QueryGroupQuery> findByQueryGroupId(Long queryGroupId);
    Flux<QueryGroupQuery> findByQueryName(String queryName);
}