package com.example.service;

import com.example.entity.MarketTrendLocation;
import com.example.dto.MarketTrendLocationInputDTO;
import com.example.dto.MarketTrendLocationOutputDTO;
import com.example.repository.MarketTrendLocationRepository;
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
 * Service class for MarketTrendLocation business logic.
 */
@Service
@RequiredArgsConstructor
public class MarketTrendLocationService {
    
    private final MarketTrendLocationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new MarketTrendLocation
     */
    @Transactional
    public Mono<MarketTrendLocationOutputDTO> create(MarketTrendLocationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                MarketTrendLocation entity = MarketTrendLocation.builder()
                    .trendId(inputDTO.getTrendId())
                    .country(inputDTO.getCountry())
                    .region(inputDTO.getRegion())
                    .city(inputDTO.getCity())
                    .jobMarketHealth(inputDTO.getJobMarketHealth())
                    .unemploymentRate(inputDTO.getUnemploymentRate())
                    .averageSalary(inputDTO.getAverageSalary())
                    .costOfLivingIndex(inputDTO.getCostOfLivingIndex())
                    .topIndustries(inputDTO.getTopIndustries())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("market_trend_location")
                            .recordId(saved.getLocationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendLocation", saved.getLocationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find MarketTrendLocation by ID
     */
    public Mono<MarketTrendLocationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendLocation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all MarketTrendLocations
     */
    public Flux<MarketTrendLocationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find MarketTrendLocations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<MarketTrendLocationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<MarketTrendLocation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "market_trend_location", groupIds);
                            Flux<MarketTrendLocation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "market_trend_location", groupIds, size, offset);
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
     * Update MarketTrendLocation
     */
    @Transactional
    public Mono<MarketTrendLocationOutputDTO> update(Long id, MarketTrendLocationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendLocation", id)))
                    .flatMap(existing -> {
                        existing.setTrendId(inputDTO.getTrendId());
                        existing.setCountry(inputDTO.getCountry());
                        existing.setRegion(inputDTO.getRegion());
                        existing.setCity(inputDTO.getCity());
                        existing.setJobMarketHealth(inputDTO.getJobMarketHealth());
                        existing.setUnemploymentRate(inputDTO.getUnemploymentRate());
                        existing.setAverageSalary(inputDTO.getAverageSalary());
                        existing.setCostOfLivingIndex(inputDTO.getCostOfLivingIndex());
                        existing.setTopIndustries(inputDTO.getTopIndustries());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendLocation", saved.getLocationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete MarketTrendLocation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendLocation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendLocation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_location", id))
            );
    }
    
    /**
     * Delete MarketTrendLocation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendLocation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendLocation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_location", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private MarketTrendLocationOutputDTO toOutputDTO(MarketTrendLocation entity) {
        return MarketTrendLocationOutputDTO.builder()
            .locationId(entity.getLocationId())
            .trendId(entity.getTrendId())
            .country(entity.getCountry())
            .region(entity.getRegion())
            .city(entity.getCity())
            .jobMarketHealth(entity.getJobMarketHealth())
            .unemploymentRate(entity.getUnemploymentRate())
            .averageSalary(entity.getAverageSalary())
            .costOfLivingIndex(entity.getCostOfLivingIndex())
            .topIndustries(entity.getTopIndustries())
            .build();
    }
}