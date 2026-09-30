package com.example.service;

import com.example.entity.AiEvaluationParameter;
import com.example.dto.AiEvaluationParameterInputDTO;
import com.example.dto.AiEvaluationParameterOutputDTO;
import com.example.repository.AiEvaluationParameterRepository;
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
 * Service class for AiEvaluationParameter business logic.
 */
@Service
@RequiredArgsConstructor
public class AiEvaluationParameterService {
    
    private final AiEvaluationParameterRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiEvaluationParameter
     */
    @Transactional
    public Mono<AiEvaluationParameterOutputDTO> create(AiEvaluationParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiEvaluationParameter entity = AiEvaluationParameter.builder()
                    .parameterName(inputDTO.getParameterName())
                    .parameterGroupId(inputDTO.getParameterGroupId())
                    .parameterValue(inputDTO.getParameterValue())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_evaluation_parameter")
                            .recordId(saved.getParameterId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiEvaluationParameter", saved.getParameterId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiEvaluationParameter by ID
     */
    public Mono<AiEvaluationParameterOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiEvaluationParameter", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiEvaluationParameters
     */
    public Flux<AiEvaluationParameterOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiEvaluationParameters with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiEvaluationParameterOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiEvaluationParameter> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_evaluation_parameter", groupIds);
                            Flux<AiEvaluationParameter> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_evaluation_parameter", groupIds, size, offset);
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
     * Update AiEvaluationParameter
     */
    @Transactional
    public Mono<AiEvaluationParameterOutputDTO> update(Long id, AiEvaluationParameterInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiEvaluationParameter", id)))
                    .flatMap(existing -> {
                        existing.setParameterName(inputDTO.getParameterName());
                        existing.setParameterGroupId(inputDTO.getParameterGroupId());
                        existing.setParameterValue(inputDTO.getParameterValue());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiEvaluationParameter", saved.getParameterId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiEvaluationParameter
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiEvaluationParameter", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiEvaluationParameter", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_evaluation_parameter", id))
            );
    }
    
    /**
     * Delete AiEvaluationParameter with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiEvaluationParameter", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiEvaluationParameter", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_evaluation_parameter", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiEvaluationParameterOutputDTO toOutputDTO(AiEvaluationParameter entity) {
        return AiEvaluationParameterOutputDTO.builder()
            .parameterId(entity.getParameterId())
            .parameterName(entity.getParameterName())
            .parameterGroupId(entity.getParameterGroupId())
            .parameterValue(entity.getParameterValue())
            .build();
    }
}