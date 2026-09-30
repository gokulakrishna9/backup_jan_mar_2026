package com.example.service;

import com.example.entity.AiUserProfileEvaluation;
import com.example.dto.AiUserProfileEvaluationInputDTO;
import com.example.dto.AiUserProfileEvaluationOutputDTO;
import com.example.repository.AiUserProfileEvaluationRepository;
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
 * Service class for AiUserProfileEvaluation business logic.
 */
@Service
@RequiredArgsConstructor
public class AiUserProfileEvaluationService {
    
    private final AiUserProfileEvaluationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiUserProfileEvaluation
     */
    @Transactional
    public Mono<AiUserProfileEvaluationOutputDTO> create(AiUserProfileEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiUserProfileEvaluation entity = AiUserProfileEvaluation.builder()
                    .userId(inputDTO.getUserId())
                    .propertyId(inputDTO.getPropertyId())
                    .evaluationSummary(inputDTO.getEvaluationSummary())
                    .rating(inputDTO.getRating())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_user_profile_evaluation")
                            .recordId(saved.getEvaluationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiUserProfileEvaluation", saved.getEvaluationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiUserProfileEvaluation by ID
     */
    public Mono<AiUserProfileEvaluationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiUserProfileEvaluation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiUserProfileEvaluations
     */
    public Flux<AiUserProfileEvaluationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiUserProfileEvaluations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiUserProfileEvaluationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiUserProfileEvaluation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_user_profile_evaluation", groupIds);
                            Flux<AiUserProfileEvaluation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_user_profile_evaluation", groupIds, size, offset);
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
     * Update AiUserProfileEvaluation
     */
    @Transactional
    public Mono<AiUserProfileEvaluationOutputDTO> update(Long id, AiUserProfileEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiUserProfileEvaluation", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setPropertyId(inputDTO.getPropertyId());
                        existing.setEvaluationSummary(inputDTO.getEvaluationSummary());
                        existing.setRating(inputDTO.getRating());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiUserProfileEvaluation", saved.getEvaluationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiUserProfileEvaluation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiUserProfileEvaluation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiUserProfileEvaluation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_user_profile_evaluation", id))
            );
    }
    
    /**
     * Delete AiUserProfileEvaluation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiUserProfileEvaluation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiUserProfileEvaluation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_user_profile_evaluation", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiUserProfileEvaluationOutputDTO toOutputDTO(AiUserProfileEvaluation entity) {
        return AiUserProfileEvaluationOutputDTO.builder()
            .evaluationId(entity.getEvaluationId())
            .userId(entity.getUserId())
            .propertyId(entity.getPropertyId())
            .evaluationSummary(entity.getEvaluationSummary())
            .rating(entity.getRating())
            .build();
    }
}