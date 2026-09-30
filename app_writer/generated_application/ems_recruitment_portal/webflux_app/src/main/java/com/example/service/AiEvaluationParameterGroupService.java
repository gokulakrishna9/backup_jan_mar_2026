package com.example.service;

import com.example.entity.AiEvaluationParameterGroup;
import com.example.dto.AiEvaluationParameterGroupInputDTO;
import com.example.dto.AiEvaluationParameterGroupOutputDTO;
import com.example.repository.AiEvaluationParameterGroupRepository;
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
 * Service class for AiEvaluationParameterGroup business logic.
 */
@Service
@RequiredArgsConstructor
public class AiEvaluationParameterGroupService {
    
    private final AiEvaluationParameterGroupRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new AiEvaluationParameterGroup
     */
    @Transactional
    public Mono<AiEvaluationParameterGroupOutputDTO> create(AiEvaluationParameterGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                AiEvaluationParameterGroup entity = AiEvaluationParameterGroup.builder()
                    .groupName(inputDTO.getGroupName())
                    .description(inputDTO.getDescription())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("ai_evaluation_parameter_group")
                            .recordId(saved.getGroupId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiEvaluationParameterGroup", saved.getGroupId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find AiEvaluationParameterGroup by ID
     */
    public Mono<AiEvaluationParameterGroupOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("AiEvaluationParameterGroup", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all AiEvaluationParameterGroups
     */
    public Flux<AiEvaluationParameterGroupOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find AiEvaluationParameterGroups with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<AiEvaluationParameterGroupOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<AiEvaluationParameterGroup> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "ai_evaluation_parameter_group", groupIds);
                            Flux<AiEvaluationParameterGroup> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "ai_evaluation_parameter_group", groupIds, size, offset);
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
     * Update AiEvaluationParameterGroup
     */
    @Transactional
    public Mono<AiEvaluationParameterGroupOutputDTO> update(Long id, AiEvaluationParameterGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiEvaluationParameterGroup", id)))
                    .flatMap(existing -> {
                        existing.setGroupName(inputDTO.getGroupName());
                        existing.setDescription(inputDTO.getDescription());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "AiEvaluationParameterGroup", saved.getGroupId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete AiEvaluationParameterGroup
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiEvaluationParameterGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiEvaluationParameterGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_evaluation_parameter_group", id))
            );
    }
    
    /**
     * Delete AiEvaluationParameterGroup with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("AiEvaluationParameterGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "AiEvaluationParameterGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("ai_evaluation_parameter_group", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private AiEvaluationParameterGroupOutputDTO toOutputDTO(AiEvaluationParameterGroup entity) {
        return AiEvaluationParameterGroupOutputDTO.builder()
            .groupId(entity.getGroupId())
            .groupName(entity.getGroupName())
            .description(entity.getDescription())
            .build();
    }
}