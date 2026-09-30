package com.jobportal.repository;

import com.jobportal.entity.SystemConfig;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public interface SystemConfigRepository extends R2dbcRepository<SystemConfig, String> {
    
    Mono<SystemConfig> findByConfigKey(String configKey);
}