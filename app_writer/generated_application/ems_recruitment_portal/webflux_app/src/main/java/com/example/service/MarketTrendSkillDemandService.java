package com.example.service;

import com.example.entity.MarketTrendSkillDemand;
import com.example.dto.MarketTrendSkillDemandInputDTO;
import com.example.dto.MarketTrendSkillDemandOutputDTO;
import com.example.repository.MarketTrendSkillDemandRepository;
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
 * Service class for MarketTrendSkillDemand business logic.
 */
@Service
@RequiredArgsConstructor
public class MarketTrendSkillDemandService {
    
    private final MarketTrendSkillDemandRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new MarketTrendSkillDemand
     */
    @Transactional
    public Mono<MarketTrendSkillDemandOutputDTO> create(MarketTrendSkillDemandInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                MarketTrendSkillDemand entity = MarketTrendSkillDemand.builder()
                    .trendId(inputDTO.getTrendId())
                    .skillName(inputDTO.getSkillName())
                    .demandLevel(inputDTO.getDemandLevel())
                    .growthRate(inputDTO.getGrowthRate())
                    .averageSalaryRange(inputDTO.getAverageSalaryRange())
                    .jobOpeningsCount(inputDTO.getJobOpeningsCount())
                    .region(inputDTO.getRegion())
                    .industry(inputDTO.getIndustry())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("market_trend_skill_demand")
                            .recordId(saved.getDemandId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendSkillDemand", saved.getDemandId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find MarketTrendSkillDemand by ID
     */
    public Mono<MarketTrendSkillDemandOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendSkillDemand", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all MarketTrendSkillDemands
     */
    public Flux<MarketTrendSkillDemandOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find MarketTrendSkillDemands with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<MarketTrendSkillDemandOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<MarketTrendSkillDemand> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "market_trend_skill_demand", groupIds);
                            Flux<MarketTrendSkillDemand> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "market_trend_skill_demand", groupIds, size, offset);
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
     * Update MarketTrendSkillDemand
     */
    @Transactional
    public Mono<MarketTrendSkillDemandOutputDTO> update(Long id, MarketTrendSkillDemandInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendSkillDemand", id)))
                    .flatMap(existing -> {
                        existing.setTrendId(inputDTO.getTrendId());
                        existing.setSkillName(inputDTO.getSkillName());
                        existing.setDemandLevel(inputDTO.getDemandLevel());
                        existing.setGrowthRate(inputDTO.getGrowthRate());
                        existing.setAverageSalaryRange(inputDTO.getAverageSalaryRange());
                        existing.setJobOpeningsCount(inputDTO.getJobOpeningsCount());
                        existing.setRegion(inputDTO.getRegion());
                        existing.setIndustry(inputDTO.getIndustry());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendSkillDemand", saved.getDemandId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete MarketTrendSkillDemand
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendSkillDemand", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendSkillDemand", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_skill_demand", id))
            );
    }
    
    /**
     * Delete MarketTrendSkillDemand with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendSkillDemand", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendSkillDemand", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_skill_demand", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private MarketTrendSkillDemandOutputDTO toOutputDTO(MarketTrendSkillDemand entity) {
        return MarketTrendSkillDemandOutputDTO.builder()
            .demandId(entity.getDemandId())
            .trendId(entity.getTrendId())
            .skillName(entity.getSkillName())
            .demandLevel(entity.getDemandLevel())
            .growthRate(entity.getGrowthRate())
            .averageSalaryRange(entity.getAverageSalaryRange())
            .jobOpeningsCount(entity.getJobOpeningsCount())
            .region(entity.getRegion())
            .industry(entity.getIndustry())
            .build();
    }
}