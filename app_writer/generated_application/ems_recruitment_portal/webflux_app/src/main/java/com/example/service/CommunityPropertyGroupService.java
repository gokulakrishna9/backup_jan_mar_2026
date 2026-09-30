package com.example.service;

import com.example.entity.CommunityPropertyGroup;
import com.example.dto.CommunityPropertyGroupInputDTO;
import com.example.dto.CommunityPropertyGroupOutputDTO;
import com.example.repository.CommunityPropertyGroupRepository;
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
 * Service class for CommunityPropertyGroup business logic.
 */
@Service
@RequiredArgsConstructor
public class CommunityPropertyGroupService {
    
    private final CommunityPropertyGroupRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CommunityPropertyGroup
     */
    @Transactional
    public Mono<CommunityPropertyGroupOutputDTO> create(CommunityPropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CommunityPropertyGroup entity = CommunityPropertyGroup.builder()
                    .groupName(inputDTO.getGroupName())
                    .groupDescription(inputDTO.getGroupDescription())
                    .communityId(inputDTO.getCommunityId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("community_property_group")
                            .recordId(saved.getGroupId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityPropertyGroup", saved.getGroupId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CommunityPropertyGroup by ID
     */
    public Mono<CommunityPropertyGroupOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityPropertyGroup", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CommunityPropertyGroups
     */
    public Flux<CommunityPropertyGroupOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CommunityPropertyGroups with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CommunityPropertyGroupOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CommunityPropertyGroup> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "community_property_group", groupIds);
                            Flux<CommunityPropertyGroup> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "community_property_group", groupIds, size, offset);
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
     * Update CommunityPropertyGroup
     */
    @Transactional
    public Mono<CommunityPropertyGroupOutputDTO> update(Long id, CommunityPropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityPropertyGroup", id)))
                    .flatMap(existing -> {
                        existing.setGroupName(inputDTO.getGroupName());
                        existing.setGroupDescription(inputDTO.getGroupDescription());
                        existing.setCommunityId(inputDTO.getCommunityId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityPropertyGroup", saved.getGroupId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CommunityPropertyGroup
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityPropertyGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityPropertyGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_property_group", id))
            );
    }
    
    /**
     * Delete CommunityPropertyGroup with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityPropertyGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityPropertyGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_property_group", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CommunityPropertyGroupOutputDTO toOutputDTO(CommunityPropertyGroup entity) {
        return CommunityPropertyGroupOutputDTO.builder()
            .groupId(entity.getGroupId())
            .groupName(entity.getGroupName())
            .groupDescription(entity.getGroupDescription())
            .communityId(entity.getCommunityId())
            .build();
    }
}