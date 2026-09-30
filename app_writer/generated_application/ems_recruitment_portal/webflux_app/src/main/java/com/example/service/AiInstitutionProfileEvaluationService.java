package com.example.service;

import com.example.entity.AiInstitutionProfileEvaluation;
import com.example.dto.AiInstitutionProfileEvaluationInputDTO;
import com.example.dto.AiInstitutionProfileEvaluationOutputDTO;
import com.example.repository.AiInstitutionProfileEvaluationRepository;
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
 * Service class for AiInstitutionProfileEvaluation business logic.
 */
@Service
@RequiredArgsConstructor
public class AiInstitutionProfileEvaluationService {
    
    private final AiInstitutionProfileEvaluationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiInstitutionProfileEvaluation
     */
    @Transactional
    public Mono<AiInstitutionProfileEvaluationOutputDTO> create(AiInstitutionProfileEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiInstitutionProfileEvaluation entity = AiInstitutionProfileEvaluation.builder()
                    .institutionId(inputDTO.getInstitutionId())
                    .evaluationSummary(inputDTO.getEvaluationSummary())
                    .rating(inputDTO.getRating())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_institution_profile_evaluation")
                            .recordId(saved.getEvaluationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiInstitutionProfileEvaluation", saved.getEvaluationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiInstitutionProfileEvaluation by ID
     */
    public Mono<AiInstitutionProfileEvaluationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiInstitutionProfileEvaluation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiInstitutionProfileEvaluations
     */
    public Flux<AiInstitutionProfileEvaluationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiInstitutionProfileEvaluations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiInstitutionProfileEvaluationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiInstitutionProfileEvaluation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_institution_profile_evaluation", groupIds);
                            Flux<AiInstitutionProfileEvaluation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_institution_profile_evaluation", groupIds, size, offset);
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
     * Update AiInstitutionProfileEvaluation
     */
    @Transactional
    public Mono<AiInstitutionProfileEvaluationOutputDTO> update(Long id, AiInstitutionProfileEvaluationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiInstitutionProfileEvaluation", id)))
                    .flatMap(existing -> {
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setEvaluationSummary(inputDTO.getEvaluationSummary());
                        existing.setRating(inputDTO.getRating());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiInstitutionProfileEvaluation", saved.getEvaluationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiInstitutionProfileEvaluation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiInstitutionProfileEvaluation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiInstitutionProfileEvaluation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_institution_profile_evaluation", id))
            );
    }
    
    /**
     * Delete AiInstitutionProfileEvaluation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiInstitutionProfileEvaluation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiInstitutionProfileEvaluation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_institution_profile_evaluation", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiInstitutionProfileEvaluationOutputDTO toOutputDTO(AiInstitutionProfileEvaluation entity) {
        return AiInstitutionProfileEvaluationOutputDTO.builder()
            .evaluationId(entity.getEvaluationId())
            .institutionId(entity.getInstitutionId())
            .evaluationSummary(entity.getEvaluationSummary())
            .rating(entity.getRating())
            .build();
    }
}