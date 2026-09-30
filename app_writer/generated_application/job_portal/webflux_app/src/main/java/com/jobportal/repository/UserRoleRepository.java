package com.jobportal.repository;

import com.jobportal.entity.UserRole;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface UserRoleRepository extends R2dbcRepository<UserRole, Long> {
    
    Flux<UserRole> findByAuthUserId(Long authUserId);
    Flux<UserRole> findByAuthUserIdAndTableName(Long authUserId, String tableName);
    Flux<UserRole> findByRole(String role);
    Mono<Void> deleteByAuthUserIdAndTableName(Long authUserId, String tableName);
}