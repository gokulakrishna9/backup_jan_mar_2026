package com.example.service;

import com.example.entity.UserProperty;
import com.example.dto.UserPropertyInputDTO;
import com.example.dto.UserPropertyOutputDTO;
import com.example.repository.UserPropertyRepository;
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
 * Service class for UserProperty business logic.
 */
@Service
@RequiredArgsConstructor
public class UserPropertyService {
    
    private final UserPropertyRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserProperty
     */
    @Transactional
    public Mono<UserPropertyOutputDTO> create(UserPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserProperty entity = UserProperty.builder()
                    .propertyName(inputDTO.getPropertyName())
                    .propertyValue(inputDTO.getPropertyValue())
                    .propertyType(inputDTO.getPropertyType())
                    .propertyDescription(inputDTO.getPropertyDescription())
                    .groupId(inputDTO.getGroupId())
                    .userId(inputDTO.getUserId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_property")
                            .recordId(saved.getPropertyId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProperty", saved.getPropertyId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserProperty by ID
     */
    public Mono<UserPropertyOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProperty", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserPropertys
     */
    public Flux<UserPropertyOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserPropertys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserPropertyOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserProperty> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_property", groupIds);
                            Flux<UserProperty> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_property", groupIds, size, offset);
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
     * Update UserProperty
     */
    @Transactional
    public Mono<UserPropertyOutputDTO> update(Long id, UserPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProperty", id)))
                    .flatMap(existing -> {
                        existing.setPropertyName(inputDTO.getPropertyName());
                        existing.setPropertyValue(inputDTO.getPropertyValue());
                        existing.setPropertyType(inputDTO.getPropertyType());
                        existing.setPropertyDescription(inputDTO.getPropertyDescription());
                        existing.setGroupId(inputDTO.getGroupId());
                        existing.setUserId(inputDTO.getUserId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProperty", saved.getPropertyId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserProperty
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_property", id))
            );
    }
    
    /**
     * Delete UserProperty with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_property", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserPropertyOutputDTO toOutputDTO(UserProperty entity) {
        return UserPropertyOutputDTO.builder()
            .propertyId(entity.getPropertyId())
            .propertyName(entity.getPropertyName())
            .propertyValue(entity.getPropertyValue())
            .propertyType(entity.getPropertyType())
            .propertyDescription(entity.getPropertyDescription())
            .groupId(entity.getGroupId())
            .userId(entity.getUserId())
            .build();
    }
}