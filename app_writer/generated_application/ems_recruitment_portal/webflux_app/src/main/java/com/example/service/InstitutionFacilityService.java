package com.example.service;

import com.example.entity.InstitutionFacility;
import com.example.dto.InstitutionFacilityInputDTO;
import com.example.dto.InstitutionFacilityOutputDTO;
import com.example.repository.InstitutionFacilityRepository;
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
 * Service class for InstitutionFacility business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionFacilityService {
    
    private final InstitutionFacilityRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new InstitutionFacility
     */
    @Transactional
    public Mono<InstitutionFacilityOutputDTO> create(InstitutionFacilityInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                InstitutionFacility entity = InstitutionFacility.builder()
                    .institutionId(inputDTO.getInstitutionId())
                    .facilityName(inputDTO.getFacilityName())
                    .facilityType(inputDTO.getFacilityType())
                    .description(inputDTO.getDescription())
                    .capacity(inputDTO.getCapacity())
                    .locationId(inputDTO.getLocationId())
                    .isAvailable(inputDTO.getIsAvailable())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("institution_facility")
                            .recordId(saved.getFacilityId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionFacility", saved.getFacilityId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find InstitutionFacility by ID
     */
    public Mono<InstitutionFacilityOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionFacility", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all InstitutionFacilitys
     */
    public Flux<InstitutionFacilityOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find InstitutionFacilitys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionFacilityOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<InstitutionFacility> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution_facility", groupIds);
                            Flux<InstitutionFacility> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution_facility", groupIds, size, offset);
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
     * Update InstitutionFacility
     */
    @Transactional
    public Mono<InstitutionFacilityOutputDTO> update(Long id, InstitutionFacilityInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionFacility", id)))
                    .flatMap(existing -> {
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setFacilityName(inputDTO.getFacilityName());
                        existing.setFacilityType(inputDTO.getFacilityType());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setCapacity(inputDTO.getCapacity());
                        existing.setLocationId(inputDTO.getLocationId());
                        existing.setIsAvailable(inputDTO.getIsAvailable());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionFacility", saved.getFacilityId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete InstitutionFacility
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionFacility", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionFacility", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_facility", id))
            );
    }
    
    /**
     * Delete InstitutionFacility with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionFacility", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionFacility", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_facility", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionFacilityOutputDTO toOutputDTO(InstitutionFacility entity) {
        return InstitutionFacilityOutputDTO.builder()
            .facilityId(entity.getFacilityId())
            .institutionId(entity.getInstitutionId())
            .facilityName(entity.getFacilityName())
            .facilityType(entity.getFacilityType())
            .description(entity.getDescription())
            .capacity(entity.getCapacity())
            .locationId(entity.getLocationId())
            .isAvailable(entity.getIsAvailable())
            .build();
    }
}