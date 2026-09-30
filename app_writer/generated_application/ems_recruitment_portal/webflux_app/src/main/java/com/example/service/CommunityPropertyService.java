package com.example.service;

import com.example.entity.CommunityProperty;
import com.example.dto.CommunityPropertyInputDTO;
import com.example.dto.CommunityPropertyOutputDTO;
import com.example.repository.CommunityPropertyRepository;
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
 * Service class for CommunityProperty business logic.
 */
@Service
@RequiredArgsConstructor
public class CommunityPropertyService {
    
    private final CommunityPropertyRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CommunityProperty
     */
    @Transactional
    public Mono<CommunityPropertyOutputDTO> create(CommunityPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CommunityProperty entity = CommunityProperty.builder()
                    .propertyName(inputDTO.getPropertyName())
                    .propertyValue(inputDTO.getPropertyValue())
                    .propertyType(inputDTO.getPropertyType())
                    .propertyDescription(inputDTO.getPropertyDescription())
                    .groupId(inputDTO.getGroupId())
                    .communityId(inputDTO.getCommunityId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("community_property")
                            .recordId(saved.getPropertyId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityProperty", saved.getPropertyId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CommunityProperty by ID
     */
    public Mono<CommunityPropertyOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityProperty", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CommunityPropertys
     */
    public Flux<CommunityPropertyOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CommunityPropertys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CommunityPropertyOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CommunityProperty> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "community_property", groupIds);
                            Flux<CommunityProperty> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "community_property", groupIds, size, offset);
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
     * Update CommunityProperty
     */
    @Transactional
    public Mono<CommunityPropertyOutputDTO> update(Long id, CommunityPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityProperty", id)))
                    .flatMap(existing -> {
                        existing.setPropertyName(inputDTO.getPropertyName());
                        existing.setPropertyValue(inputDTO.getPropertyValue());
                        existing.setPropertyType(inputDTO.getPropertyType());
                        existing.setPropertyDescription(inputDTO.getPropertyDescription());
                        existing.setGroupId(inputDTO.getGroupId());
                        existing.setCommunityId(inputDTO.getCommunityId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityProperty", saved.getPropertyId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CommunityProperty
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_property", id))
            );
    }
    
    /**
     * Delete CommunityProperty with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_property", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CommunityPropertyOutputDTO toOutputDTO(CommunityProperty entity) {
        return CommunityPropertyOutputDTO.builder()
            .propertyId(entity.getPropertyId())
            .propertyName(entity.getPropertyName())
            .propertyValue(entity.getPropertyValue())
            .propertyType(entity.getPropertyType())
            .propertyDescription(entity.getPropertyDescription())
            .groupId(entity.getGroupId())
            .communityId(entity.getCommunityId())
            .build();
    }
}