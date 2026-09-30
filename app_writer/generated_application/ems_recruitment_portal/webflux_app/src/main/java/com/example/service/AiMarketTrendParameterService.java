package com.example.service;

import com.example.entity.AiMarketTrendParameter;
import com.example.dto.AiMarketTrendParameterInputDTO;
import com.example.dto.AiMarketTrendParameterOutputDTO;
import com.example.repository.AiMarketTrendParameterRepository;
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
 * Service class for AiMarketTrendParameter business logic.
 */
@Service
@RequiredArgsConstructor
public class AiMarketTrendParameterService {
    
    private final AiMarketTrendParameterRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiMarketTrendParameter
     */
    @Transactional
    public Mono<AiMarketTrendParameterOutputDTO> create(AiMarketTrendParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiMarketTrendParameter entity = AiMarketTrendParameter.builder()
                    .parameterName(inputDTO.getParameterName())
                    .parameterValue(inputDTO.getParameterValue())
                    .groupId(inputDTO.getGroupId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_market_trend_parameter")
                            .recordId(saved.getParameterId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiMarketTrendParameter", saved.getParameterId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiMarketTrendParameter by ID
     */
    public Mono<AiMarketTrendParameterOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiMarketTrendParameter", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiMarketTrendParameters
     */
    public Flux<AiMarketTrendParameterOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiMarketTrendParameters with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiMarketTrendParameterOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiMarketTrendParameter> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_market_trend_parameter", groupIds);
                            Flux<AiMarketTrendParameter> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_market_trend_parameter", groupIds, size, offset);
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
     * Update AiMarketTrendParameter
     */
    @Transactional
    public Mono<AiMarketTrendParameterOutputDTO> update(Long id, AiMarketTrendParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiMarketTrendParameter", id)))
                    .flatMap(existing -> {
                        existing.setParameterName(inputDTO.getParameterName());
                        existing.setParameterValue(inputDTO.getParameterValue());
                        existing.setGroupId(inputDTO.getGroupId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiMarketTrendParameter", saved.getParameterId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiMarketTrendParameter
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiMarketTrendParameter", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiMarketTrendParameter", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_market_trend_parameter", id))
            );
    }
    
    /**
     * Delete AiMarketTrendParameter with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiMarketTrendParameter", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiMarketTrendParameter", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_market_trend_parameter", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiMarketTrendParameterOutputDTO toOutputDTO(AiMarketTrendParameter entity) {
        return AiMarketTrendParameterOutputDTO.builder()
            .parameterId(entity.getParameterId())
            .parameterName(entity.getParameterName())
            .parameterValue(entity.getParameterValue())
            .groupId(entity.getGroupId())
            .build();
    }
}