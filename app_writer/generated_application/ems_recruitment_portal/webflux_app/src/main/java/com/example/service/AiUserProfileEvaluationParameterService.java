package com.example.service;

import com.example.entity.AiUserProfileEvaluationParameter;
import com.example.dto.AiUserProfileEvaluationParameterInputDTO;
import com.example.dto.AiUserProfileEvaluationParameterOutputDTO;
import com.example.repository.AiUserProfileEvaluationParameterRepository;
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
 * Service class for AiUserProfileEvaluationParameter business logic.
 */
@Service
@RequiredArgsConstructor
public class AiUserProfileEvaluationParameterService {
    
    private final AiUserProfileEvaluationParameterRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiUserProfileEvaluationParameter
     */
    @Transactional
    public Mono<AiUserProfileEvaluationParameterOutputDTO> create(AiUserProfileEvaluationParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiUserProfileEvaluationParameter entity = AiUserProfileEvaluationParameter.builder()
                    .parameterName(inputDTO.getParameterName())
                    .groupId(inputDTO.getGroupId())
                    .parameterValue(inputDTO.getParameterValue())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_user_profile_evaluation_parameter")
                            .recordId(saved.getParameterId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiUserProfileEvaluationParameter", saved.getParameterId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiUserProfileEvaluationParameter by ID
     */
    public Mono<AiUserProfileEvaluationParameterOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiUserProfileEvaluationParameter", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiUserProfileEvaluationParameters
     */
    public Flux<AiUserProfileEvaluationParameterOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiUserProfileEvaluationParameters with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiUserProfileEvaluationParameterOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiUserProfileEvaluationParameter> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_user_profile_evaluation_parameter", groupIds);
                            Flux<AiUserProfileEvaluationParameter> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_user_profile_evaluation_parameter", groupIds, size, offset);
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
     * Update AiUserProfileEvaluationParameter
     */
    @Transactional
    public Mono<AiUserProfileEvaluationParameterOutputDTO> update(Long id, AiUserProfileEvaluationParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiUserProfileEvaluationParameter", id)))
                    .flatMap(existing -> {
                        existing.setParameterName(inputDTO.getParameterName());
                        existing.setGroupId(inputDTO.getGroupId());
                        existing.setParameterValue(inputDTO.getParameterValue());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiUserProfileEvaluationParameter", saved.getParameterId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiUserProfileEvaluationParameter
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiUserProfileEvaluationParameter", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiUserProfileEvaluationParameter", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_user_profile_evaluation_parameter", id))
            );
    }
    
    /**
     * Delete AiUserProfileEvaluationParameter with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiUserProfileEvaluationParameter", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiUserProfileEvaluationParameter", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_user_profile_evaluation_parameter", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiUserProfileEvaluationParameterOutputDTO toOutputDTO(AiUserProfileEvaluationParameter entity) {
        return AiUserProfileEvaluationParameterOutputDTO.builder()
            .parameterId(entity.getParameterId())
            .parameterName(entity.getParameterName())
            .groupId(entity.getGroupId())
            .parameterValue(entity.getParameterValue())
            .build();
    }
}