package com.onlineshopping.repository;

import com.onlineshopping.entity.OAuth2Provider;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface OAuth2ProviderRepository extends ReactiveCrudRepository<OAuth2Provider, Long> {
    
    Mono<OAuth2Provider> findByProviderName(String providerName);
    
    @Query("SELECT * FROM oauth2_provider WHERE is_enabled = true")
    Flux<OAuth2Provider> findAllEnabled();
}