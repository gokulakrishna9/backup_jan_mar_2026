package com.example.service;

import com.example.entity.UserPropertyGroup;
import com.example.dto.UserPropertyGroupInputDTO;
import com.example.dto.UserPropertyGroupOutputDTO;
import com.example.repository.UserPropertyGroupRepository;
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
 * Service class for UserPropertyGroup business logic.
 */
@Service
@RequiredArgsConstructor
public class UserPropertyGroupService {
    
    private final UserPropertyGroupRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserPropertyGroup
     */
    @Transactional
    public Mono<UserPropertyGroupOutputDTO> create(UserPropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserPropertyGroup entity = UserPropertyGroup.builder()
                    .groupName(inputDTO.getGroupName())
                    .groupDescription(inputDTO.getGroupDescription())
                    .userId(inputDTO.getUserId())
                    .isActive(inputDTO.getIsActive())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_property_group")
                            .recordId(saved.getGroupId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserPropertyGroup", saved.getGroupId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserPropertyGroup by ID
     */
    public Mono<UserPropertyGroupOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserPropertyGroup", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserPropertyGroups
     */
    public Flux<UserPropertyGroupOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserPropertyGroups with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserPropertyGroupOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserPropertyGroup> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_property_group", groupIds);
                            Flux<UserPropertyGroup> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_property_group", groupIds, size, offset);
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
     * Update UserPropertyGroup
     */
    @Transactional
    public Mono<UserPropertyGroupOutputDTO> update(Long id, UserPropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserPropertyGroup", id)))
                    .flatMap(existing -> {
                        existing.setGroupName(inputDTO.getGroupName());
                        existing.setGroupDescription(inputDTO.getGroupDescription());
                        existing.setUserId(inputDTO.getUserId());
                        existing.setIsActive(inputDTO.getIsActive());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserPropertyGroup", saved.getGroupId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserPropertyGroup
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserPropertyGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserPropertyGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_property_group", id))
            );
    }
    
    /**
     * Delete UserPropertyGroup with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserPropertyGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserPropertyGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_property_group", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserPropertyGroupOutputDTO toOutputDTO(UserPropertyGroup entity) {
        return UserPropertyGroupOutputDTO.builder()
            .groupId(entity.getGroupId())
            .groupName(entity.getGroupName())
            .groupDescription(entity.getGroupDescription())
            .userId(entity.getUserId())
            .isActive(entity.getIsActive())
            .build();
    }
}