package com.example.service;

import com.example.entity.AiJobRecommendation;
import com.example.dto.AiJobRecommendationInputDTO;
import com.example.dto.AiJobRecommendationOutputDTO;
import com.example.repository.AiJobRecommendationRepository;
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
 * Service class for AiJobRecommendation business logic.
 */
@Service
@RequiredArgsConstructor
public class AiJobRecommendationService {
    
    private final AiJobRecommendationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiJobRecommendation
     */
    @Transactional
    public Mono<AiJobRecommendationOutputDTO> create(AiJobRecommendationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiJobRecommendation entity = AiJobRecommendation.builder()
                    .jobPostId(inputDTO.getJobPostId())
                    .profileId(inputDTO.getProfileId())
                    .preferenceRating(inputDTO.getPreferenceRating())
                    .recommendationSummary(inputDTO.getRecommendationSummary())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_job_recommendation")
                            .recordId(saved.getPreferenceId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiJobRecommendation", saved.getPreferenceId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiJobRecommendation by ID
     */
    public Mono<AiJobRecommendationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiJobRecommendation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiJobRecommendations
     */
    public Flux<AiJobRecommendationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiJobRecommendations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiJobRecommendationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiJobRecommendation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_job_recommendation", groupIds);
                            Flux<AiJobRecommendation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_job_recommendation", groupIds, size, offset);
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
     * Update AiJobRecommendation
     */
    @Transactional
    public Mono<AiJobRecommendationOutputDTO> update(Long id, AiJobRecommendationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiJobRecommendation", id)))
                    .flatMap(existing -> {
                        existing.setJobPostId(inputDTO.getJobPostId());
                        existing.setProfileId(inputDTO.getProfileId());
                        existing.setPreferenceRating(inputDTO.getPreferenceRating());
                        existing.setRecommendationSummary(inputDTO.getRecommendationSummary());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiJobRecommendation", saved.getPreferenceId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiJobRecommendation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiJobRecommendation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiJobRecommendation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_job_recommendation", id))
            );
    }
    
    /**
     * Delete AiJobRecommendation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiJobRecommendation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiJobRecommendation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_job_recommendation", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiJobRecommendationOutputDTO toOutputDTO(AiJobRecommendation entity) {
        return AiJobRecommendationOutputDTO.builder()
            .preferenceId(entity.getPreferenceId())
            .jobPostId(entity.getJobPostId())
            .profileId(entity.getProfileId())
            .preferenceRating(entity.getPreferenceRating())
            .recommendationSummary(entity.getRecommendationSummary())
            .build();
    }
}