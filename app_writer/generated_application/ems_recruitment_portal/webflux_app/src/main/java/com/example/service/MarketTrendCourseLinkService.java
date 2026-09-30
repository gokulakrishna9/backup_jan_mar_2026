package com.example.service;

import com.example.entity.MarketTrendCourseLink;
import com.example.dto.MarketTrendCourseLinkInputDTO;
import com.example.dto.MarketTrendCourseLinkOutputDTO;
import com.example.repository.MarketTrendCourseLinkRepository;
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
 * Service class for MarketTrendCourseLink business logic.
 */
@Service
@RequiredArgsConstructor
public class MarketTrendCourseLinkService {
    
    private final MarketTrendCourseLinkRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new MarketTrendCourseLink
     */
    @Transactional
    public Mono<MarketTrendCourseLinkOutputDTO> create(MarketTrendCourseLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                MarketTrendCourseLink entity = MarketTrendCourseLink.builder()
                    .trendId(inputDTO.getTrendId())
                    .courseId(inputDTO.getCourseId())
                    .relevanceScore(inputDTO.getRelevanceScore())
                    .demandLevel(inputDTO.getDemandLevel())
                    .recommendationReason(inputDTO.getRecommendationReason())
                    .aiGenerated(inputDTO.getAiGenerated())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("market_trend_course_link")
                            .recordId(saved.getLinkId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendCourseLink", saved.getLinkId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find MarketTrendCourseLink by ID
     */
    public Mono<MarketTrendCourseLinkOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendCourseLink", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all MarketTrendCourseLinks
     */
    public Flux<MarketTrendCourseLinkOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find MarketTrendCourseLinks with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<MarketTrendCourseLinkOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<MarketTrendCourseLink> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "market_trend_course_link", groupIds);
                            Flux<MarketTrendCourseLink> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "market_trend_course_link", groupIds, size, offset);
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
     * Update MarketTrendCourseLink
     */
    @Transactional
    public Mono<MarketTrendCourseLinkOutputDTO> update(Long id, MarketTrendCourseLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendCourseLink", id)))
                    .flatMap(existing -> {
                        existing.setTrendId(inputDTO.getTrendId());
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setRelevanceScore(inputDTO.getRelevanceScore());
                        existing.setDemandLevel(inputDTO.getDemandLevel());
                        existing.setRecommendationReason(inputDTO.getRecommendationReason());
                        existing.setAiGenerated(inputDTO.getAiGenerated());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendCourseLink", saved.getLinkId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete MarketTrendCourseLink
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendCourseLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendCourseLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_course_link", id))
            );
    }
    
    /**
     * Delete MarketTrendCourseLink with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendCourseLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendCourseLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_course_link", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private MarketTrendCourseLinkOutputDTO toOutputDTO(MarketTrendCourseLink entity) {
        return MarketTrendCourseLinkOutputDTO.builder()
            .linkId(entity.getLinkId())
            .trendId(entity.getTrendId())
            .courseId(entity.getCourseId())
            .relevanceScore(entity.getRelevanceScore())
            .demandLevel(entity.getDemandLevel())
            .recommendationReason(entity.getRecommendationReason())
            .aiGenerated(entity.getAiGenerated())
            .build();
    }
}