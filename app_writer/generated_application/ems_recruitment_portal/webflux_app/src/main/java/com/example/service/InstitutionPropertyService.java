package com.example.service;

import com.example.entity.InstitutionProperty;
import com.example.dto.InstitutionPropertyInputDTO;
import com.example.dto.InstitutionPropertyOutputDTO;
import com.example.repository.InstitutionPropertyRepository;
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
 * Service class for InstitutionProperty business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionPropertyService {
    
    private final InstitutionPropertyRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new InstitutionProperty
     */
    @Transactional
    public Mono<InstitutionPropertyOutputDTO> create(InstitutionPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                InstitutionProperty entity = InstitutionProperty.builder()
                    .propertyName(inputDTO.getPropertyName())
                    .propertyValue(inputDTO.getPropertyValue())
                    .propertyType(inputDTO.getPropertyType())
                    .propertyDescription(inputDTO.getPropertyDescription())
                    .groupId(inputDTO.getGroupId())
                    .institutionId(inputDTO.getInstitutionId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("institution_property")
                            .recordId(saved.getPropertyId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionProperty", saved.getPropertyId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find InstitutionProperty by ID
     */
    public Mono<InstitutionPropertyOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionProperty", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all InstitutionPropertys
     */
    public Flux<InstitutionPropertyOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find InstitutionPropertys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionPropertyOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<InstitutionProperty> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution_property", groupIds);
                            Flux<InstitutionProperty> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution_property", groupIds, size, offset);
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
     * Update InstitutionProperty
     */
    @Transactional
    public Mono<InstitutionPropertyOutputDTO> update(Long id, InstitutionPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionProperty", id)))
                    .flatMap(existing -> {
                        existing.setPropertyName(inputDTO.getPropertyName());
                        existing.setPropertyValue(inputDTO.getPropertyValue());
                        existing.setPropertyType(inputDTO.getPropertyType());
                        existing.setPropertyDescription(inputDTO.getPropertyDescription());
                        existing.setGroupId(inputDTO.getGroupId());
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionProperty", saved.getPropertyId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete InstitutionProperty
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_property", id))
            );
    }
    
    /**
     * Delete InstitutionProperty with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_property", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionPropertyOutputDTO toOutputDTO(InstitutionProperty entity) {
        return InstitutionPropertyOutputDTO.builder()
            .propertyId(entity.getPropertyId())
            .propertyName(entity.getPropertyName())
            .propertyValue(entity.getPropertyValue())
            .propertyType(entity.getPropertyType())
            .propertyDescription(entity.getPropertyDescription())
            .groupId(entity.getGroupId())
            .institutionId(entity.getInstitutionId())
            .build();
    }
}