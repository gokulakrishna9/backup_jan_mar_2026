package com.example.service;

import com.example.entity.MarketTrendIndustry;
import com.example.dto.MarketTrendIndustryInputDTO;
import com.example.dto.MarketTrendIndustryOutputDTO;
import com.example.repository.MarketTrendIndustryRepository;
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
 * Service class for MarketTrendIndustry business logic.
 */
@Service
@RequiredArgsConstructor
public class MarketTrendIndustryService {
    
    private final MarketTrendIndustryRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new MarketTrendIndustry
     */
    @Transactional
    public Mono<MarketTrendIndustryOutputDTO> create(MarketTrendIndustryInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                MarketTrendIndustry entity = MarketTrendIndustry.builder()
                    .trendId(inputDTO.getTrendId())
                    .industryName(inputDTO.getIndustryName())
                    .description(inputDTO.getDescription())
                    .growthRate(inputDTO.getGrowthRate())
                    .marketSize(inputDTO.getMarketSize())
                    .emergingTechnologies(inputDTO.getEmergingTechnologies())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("market_trend_industry")
                            .recordId(saved.getIndustryId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendIndustry", saved.getIndustryId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find MarketTrendIndustry by ID
     */
    public Mono<MarketTrendIndustryOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendIndustry", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all MarketTrendIndustrys
     */
    public Flux<MarketTrendIndustryOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find MarketTrendIndustrys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<MarketTrendIndustryOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<MarketTrendIndustry> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "market_trend_industry", groupIds);
                            Flux<MarketTrendIndustry> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "market_trend_industry", groupIds, size, offset);
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
     * Update MarketTrendIndustry
     */
    @Transactional
    public Mono<MarketTrendIndustryOutputDTO> update(Long id, MarketTrendIndustryInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendIndustry", id)))
                    .flatMap(existing -> {
                        existing.setTrendId(inputDTO.getTrendId());
                        existing.setIndustryName(inputDTO.getIndustryName());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setGrowthRate(inputDTO.getGrowthRate());
                        existing.setMarketSize(inputDTO.getMarketSize());
                        existing.setEmergingTechnologies(inputDTO.getEmergingTechnologies());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendIndustry", saved.getIndustryId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete MarketTrendIndustry
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendIndustry", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendIndustry", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_industry", id))
            );
    }
    
    /**
     * Delete MarketTrendIndustry with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendIndustry", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendIndustry", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_industry", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private MarketTrendIndustryOutputDTO toOutputDTO(MarketTrendIndustry entity) {
        return MarketTrendIndustryOutputDTO.builder()
            .industryId(entity.getIndustryId())
            .trendId(entity.getTrendId())
            .industryName(entity.getIndustryName())
            .description(entity.getDescription())
            .growthRate(entity.getGrowthRate())
            .marketSize(entity.getMarketSize())
            .emergingTechnologies(entity.getEmergingTechnologies())
            .build();
    }
}