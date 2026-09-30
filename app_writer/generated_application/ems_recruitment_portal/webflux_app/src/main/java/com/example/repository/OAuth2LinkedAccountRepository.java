package com.example.repository;

import com.example.entity.OAuth2LinkedAccount;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface OAuth2LinkedAccountRepository extends ReactiveCrudRepository<OAuth2LinkedAccount, Long> {
    
    @Query("SELECT * FROM oauth2_linked_account WHERE auth_user_id = :authUserId")
    Flux<OAuth2LinkedAccount> findByAuthUserId(Long authUserId);
    
    @Query("SELECT * FROM oauth2_linked_account WHERE provider_id = :providerId AND provider_user_id = :providerUserId")
    Mono<OAuth2LinkedAccount> findByProviderAndUserId(Long providerId, String providerUserId);
    
    @Query("SELECT * FROM oauth2_linked_account WHERE provider_email = :email")
    Flux<OAuth2LinkedAccount> findByProviderEmail(String email);
}