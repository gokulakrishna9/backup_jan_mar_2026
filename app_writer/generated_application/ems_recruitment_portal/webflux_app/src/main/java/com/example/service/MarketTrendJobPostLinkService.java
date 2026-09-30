package com.example.service;

import com.example.entity.MarketTrendJobPostLink;
import com.example.dto.MarketTrendJobPostLinkInputDTO;
import com.example.dto.MarketTrendJobPostLinkOutputDTO;
import com.example.repository.MarketTrendJobPostLinkRepository;
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
 * Service class for MarketTrendJobPostLink business logic.
 */
@Service
@RequiredArgsConstructor
public class MarketTrendJobPostLinkService {
    
    private final MarketTrendJobPostLinkRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new MarketTrendJobPostLink
     */
    @Transactional
    public Mono<MarketTrendJobPostLinkOutputDTO> create(MarketTrendJobPostLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                MarketTrendJobPostLink entity = MarketTrendJobPostLink.builder()
                    .trendId(inputDTO.getTrendId())
                    .jobPostId(inputDTO.getJobPostId())
                    .relevanceScore(inputDTO.getRelevanceScore())
                    .growthPotential(inputDTO.getGrowthPotential())
                    .salaryTrend(inputDTO.getSalaryTrend())
                    .aiGenerated(inputDTO.getAiGenerated())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("market_trend_job_post_link")
                            .recordId(saved.getLinkId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendJobPostLink", saved.getLinkId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find MarketTrendJobPostLink by ID
     */
    public Mono<MarketTrendJobPostLinkOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendJobPostLink", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all MarketTrendJobPostLinks
     */
    public Flux<MarketTrendJobPostLinkOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find MarketTrendJobPostLinks with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<MarketTrendJobPostLinkOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<MarketTrendJobPostLink> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "market_trend_job_post_link", groupIds);
                            Flux<MarketTrendJobPostLink> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "market_trend_job_post_link", groupIds, size, offset);
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
     * Update MarketTrendJobPostLink
     */
    @Transactional
    public Mono<MarketTrendJobPostLinkOutputDTO> update(Long id, MarketTrendJobPostLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendJobPostLink", id)))
                    .flatMap(existing -> {
                        existing.setTrendId(inputDTO.getTrendId());
                        existing.setJobPostId(inputDTO.getJobPostId());
                        existing.setRelevanceScore(inputDTO.getRelevanceScore());
                        existing.setGrowthPotential(inputDTO.getGrowthPotential());
                        existing.setSalaryTrend(inputDTO.getSalaryTrend());
                        existing.setAiGenerated(inputDTO.getAiGenerated());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendJobPostLink", saved.getLinkId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete MarketTrendJobPostLink
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendJobPostLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendJobPostLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_job_post_link", id))
            );
    }
    
    /**
     * Delete MarketTrendJobPostLink with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendJobPostLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendJobPostLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_job_post_link", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private MarketTrendJobPostLinkOutputDTO toOutputDTO(MarketTrendJobPostLink entity) {
        return MarketTrendJobPostLinkOutputDTO.builder()
            .linkId(entity.getLinkId())
            .trendId(entity.getTrendId())
            .jobPostId(entity.getJobPostId())
            .relevanceScore(entity.getRelevanceScore())
            .growthPotential(entity.getGrowthPotential())
            .salaryTrend(entity.getSalaryTrend())
            .aiGenerated(entity.getAiGenerated())
            .build();
    }
}