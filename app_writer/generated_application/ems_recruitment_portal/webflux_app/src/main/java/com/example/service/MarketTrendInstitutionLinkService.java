package com.example.service;

import com.example.entity.MarketTrendInstitutionLink;
import com.example.dto.MarketTrendInstitutionLinkInputDTO;
import com.example.dto.MarketTrendInstitutionLinkOutputDTO;
import com.example.repository.MarketTrendInstitutionLinkRepository;
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
 * Service class for MarketTrendInstitutionLink business logic.
 */
@Service
@RequiredArgsConstructor
public class MarketTrendInstitutionLinkService {
    
    private final MarketTrendInstitutionLinkRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new MarketTrendInstitutionLink
     */
    @Transactional
    public Mono<MarketTrendInstitutionLinkOutputDTO> create(MarketTrendInstitutionLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                MarketTrendInstitutionLink entity = MarketTrendInstitutionLink.builder()
                    .trendId(inputDTO.getTrendId())
                    .institutionId(inputDTO.getInstitutionId())
                    .relevanceScore(inputDTO.getRelevanceScore())
                    .specializationAreas(inputDTO.getSpecializationAreas())
                    .partnershipOpportunities(inputDTO.getPartnershipOpportunities())
                    .aiGenerated(inputDTO.getAiGenerated())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("market_trend_institution_link")
                            .recordId(saved.getLinkId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendInstitutionLink", saved.getLinkId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find MarketTrendInstitutionLink by ID
     */
    public Mono<MarketTrendInstitutionLinkOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendInstitutionLink", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all MarketTrendInstitutionLinks
     */
    public Flux<MarketTrendInstitutionLinkOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find MarketTrendInstitutionLinks with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<MarketTrendInstitutionLinkOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<MarketTrendInstitutionLink> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "market_trend_institution_link", groupIds);
                            Flux<MarketTrendInstitutionLink> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "market_trend_institution_link", groupIds, size, offset);
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
     * Update MarketTrendInstitutionLink
     */
    @Transactional
    public Mono<MarketTrendInstitutionLinkOutputDTO> update(Long id, MarketTrendInstitutionLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendInstitutionLink", id)))
                    .flatMap(existing -> {
                        existing.setTrendId(inputDTO.getTrendId());
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setRelevanceScore(inputDTO.getRelevanceScore());
                        existing.setSpecializationAreas(inputDTO.getSpecializationAreas());
                        existing.setPartnershipOpportunities(inputDTO.getPartnershipOpportunities());
                        existing.setAiGenerated(inputDTO.getAiGenerated());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendInstitutionLink", saved.getLinkId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete MarketTrendInstitutionLink
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendInstitutionLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendInstitutionLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_institution_link", id))
            );
    }
    
    /**
     * Delete MarketTrendInstitutionLink with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendInstitutionLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendInstitutionLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_institution_link", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private MarketTrendInstitutionLinkOutputDTO toOutputDTO(MarketTrendInstitutionLink entity) {
        return MarketTrendInstitutionLinkOutputDTO.builder()
            .linkId(entity.getLinkId())
            .trendId(entity.getTrendId())
            .institutionId(entity.getInstitutionId())
            .relevanceScore(entity.getRelevanceScore())
            .specializationAreas(entity.getSpecializationAreas())
            .partnershipOpportunities(entity.getPartnershipOpportunities())
            .aiGenerated(entity.getAiGenerated())
            .build();
    }
}