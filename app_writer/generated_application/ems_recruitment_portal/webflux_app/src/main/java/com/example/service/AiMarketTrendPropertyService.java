package com.example.service;

import com.example.entity.AiMarketTrendProperty;
import com.example.dto.AiMarketTrendPropertyInputDTO;
import com.example.dto.AiMarketTrendPropertyOutputDTO;
import com.example.repository.AiMarketTrendPropertyRepository;
import com.example.exception.EntityNotFoundException;
import com.example.dto.PageResponse;
import com.example.repository.RecordOwnerRepository;
import com.example.repository.QueryGroupRecordRepository;
import com.example.repository.QueryGroupMemberRepository;
import com.example.entity.RecordOwner;
import com.example.security.SecurityContextHolder;
import com.example.service.ActivityTrackingService;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Service class for AiMarketTrendProperty business logic.
 */
@Service
@RequiredArgsConstructor
public class AiMarketTrendPropertyService {
    
    private final AiMarketTrendPropertyRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiMarketTrendProperty
     */
    @Transactional
    public Mono<AiMarketTrendPropertyOutputDTO> create(AiMarketTrendPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiMarketTrendProperty entity = AiMarketTrendProperty.builder()
                    .trendName(inputDTO.getTrendName())
                    .trendDescription(inputDTO.getTrendDescription())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_market_trend_property")
                            .recordId(saved.getTrendId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiMarketTrendProperty", saved.getTrendId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiMarketTrendProperty by ID
     */
    public Mono<AiMarketTrendPropertyOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiMarketTrendProperty", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiMarketTrendPropertys
     */
    public Flux<AiMarketTrendPropertyOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiMarketTrendPropertys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiMarketTrendPropertyOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiMarketTrendProperty> dataMono = repository.findAllPaged(size, offset);
                    return countMono.flatMap(total ->
                        dataMono.map(this::toOutputDTO)
                            .collectList()
                            .map(content -> PageResponse.of(content, total, page, size))
                    );
                } else {
                    Long authUserId = user.getAuthUserId();
                    // USER role: filter by ownership (record_owner) OR query group sharing (query_group_record)
                    return queryGroupMemberRepository.findByAuthUserId(authUserId)
                        .map(member -> member.getQueryGroupId())
                        .collectList()
                        .flatMap(groupIds -> {
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_market_trend_property", groupIds);
                            Flux<AiMarketTrendProperty> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_market_trend_property", groupIds, size, offset);
                            return countMono.flatMap(total ->
                                dataMono.map(this::toOutputDTO)
                                    .collectList()
                                    .map(content -> PageResponse.of(content, total, page, size))
                            );
                        });
                }
            });
    }
    
    /**
     * Update AiMarketTrendProperty
     */
    @Transactional
    public Mono<AiMarketTrendPropertyOutputDTO> update(Long id, AiMarketTrendPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiMarketTrendProperty", id)))
                    .flatMap(existing -> {
                        existing.setTrendName(inputDTO.getTrendName());
                        existing.setTrendDescription(inputDTO.getTrendDescription());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiMarketTrendProperty", saved.getTrendId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiMarketTrendProperty
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiMarketTrendProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiMarketTrendProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_market_trend_property", id))
            );
    }
    
    /**
     * Delete AiMarketTrendProperty with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiMarketTrendProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiMarketTrendProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_market_trend_property", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiMarketTrendPropertyOutputDTO toOutputDTO(AiMarketTrendProperty entity) {
        return AiMarketTrendPropertyOutputDTO.builder()
            .trendId(entity.getTrendId())
            .trendName(entity.getTrendName())
            .trendDescription(entity.getTrendDescription())
            .build();
    }
}