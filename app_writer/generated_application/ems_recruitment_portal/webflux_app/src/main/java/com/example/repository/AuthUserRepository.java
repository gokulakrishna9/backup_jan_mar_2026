package com.example.repository;

import com.example.entity.AuthUser;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;

@Repository
public interface AuthUserRepository extends R2dbcRepository<AuthUser, Long> {
    
    Mono<AuthUser> findByUsername(String username);
    Mono<AuthUser> findByEmail(String email);
    Flux<AuthUser> findByIsActive(Boolean isActive);
    Mono<Boolean> existsByUsername(String username);
    Mono<Boolean> existsByEmail(String email);
}