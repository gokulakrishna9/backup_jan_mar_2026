package com.example.service;

import com.example.entity.AiCommunityPostEvaluation;
import com.example.dto.AiCommunityPostEvaluationInputDTO;
import com.example.dto.AiCommunityPostEvaluationOutputDTO;
import com.example.repository.AiCommunityPostEvaluationRepository;
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
 * Service class for AiCommunityPostEvaluation business logic.
 */
@Service
@RequiredArgsConstructor
public class AiCommunityPostEvaluationService {
    
    private final AiCommunityPostEvaluationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiCommunityPostEvaluation
     */
    @Transactional
    public Mono<AiCommunityPostEvaluationOutputDTO> create(AiCommunityPostEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiCommunityPostEvaluation entity = AiCommunityPostEvaluation.builder()
                    .postId(inputDTO.getPostId())
                    .evaluationSummary(inputDTO.getEvaluationSummary())
                    .rating(inputDTO.getRating())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_community_post_evaluation")
                            .recordId(saved.getEvaluationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiCommunityPostEvaluation", saved.getEvaluationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiCommunityPostEvaluation by ID
     */
    public Mono<AiCommunityPostEvaluationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiCommunityPostEvaluation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiCommunityPostEvaluations
     */
    public Flux<AiCommunityPostEvaluationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiCommunityPostEvaluations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiCommunityPostEvaluationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiCommunityPostEvaluation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_community_post_evaluation", groupIds);
                            Flux<AiCommunityPostEvaluation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_community_post_evaluation", groupIds, size, offset);
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
     * Update AiCommunityPostEvaluation
     */
    @Transactional
    public Mono<AiCommunityPostEvaluationOutputDTO> update(Long id, AiCommunityPostEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiCommunityPostEvaluation", id)))
                    .flatMap(existing -> {
                        existing.setPostId(inputDTO.getPostId());
                        existing.setEvaluationSummary(inputDTO.getEvaluationSummary());
                        existing.setRating(inputDTO.getRating());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiCommunityPostEvaluation", saved.getEvaluationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiCommunityPostEvaluation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiCommunityPostEvaluation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiCommunityPostEvaluation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_community_post_evaluation", id))
            );
    }
    
    /**
     * Delete AiCommunityPostEvaluation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiCommunityPostEvaluation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiCommunityPostEvaluation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_community_post_evaluation", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiCommunityPostEvaluationOutputDTO toOutputDTO(AiCommunityPostEvaluation entity) {
        return AiCommunityPostEvaluationOutputDTO.builder()
            .evaluationId(entity.getEvaluationId())
            .postId(entity.getPostId())
            .evaluationSummary(entity.getEvaluationSummary())
            .rating(entity.getRating())
            .build();
    }
}