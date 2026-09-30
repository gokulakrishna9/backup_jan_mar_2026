package com.example.service;

import com.example.entity.InstitutionLocation;
import com.example.dto.InstitutionLocationInputDTO;
import com.example.dto.InstitutionLocationOutputDTO;
import com.example.repository.InstitutionLocationRepository;
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
 * Service class for InstitutionLocation business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionLocationService {
    
    private final InstitutionLocationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new InstitutionLocation
     */
    @Transactional
    public Mono<InstitutionLocationOutputDTO> create(InstitutionLocationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                InstitutionLocation entity = InstitutionLocation.builder()
                    .institutionId(inputDTO.getInstitutionId())
                    .locationType(inputDTO.getLocationType())
                    .addressLine1(inputDTO.getAddressLine1())
                    .addressLine2(inputDTO.getAddressLine2())
                    .city(inputDTO.getCity())
                    .stateProvince(inputDTO.getStateProvince())
                    .country(inputDTO.getCountry())
                    .postalCode(inputDTO.getPostalCode())
                    .latitude(inputDTO.getLatitude())
                    .longitude(inputDTO.getLongitude())
                    .isPrimary(inputDTO.getIsPrimary())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("institution_location")
                            .recordId(saved.getLocationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionLocation", saved.getLocationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find InstitutionLocation by ID
     */
    public Mono<InstitutionLocationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionLocation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all InstitutionLocations
     */
    public Flux<InstitutionLocationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find InstitutionLocations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionLocationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<InstitutionLocation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution_location", groupIds);
                            Flux<InstitutionLocation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution_location", groupIds, size, offset);
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
     * Update InstitutionLocation
     */
    @Transactional
    public Mono<InstitutionLocationOutputDTO> update(Long id, InstitutionLocationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionLocation", id)))
                    .flatMap(existing -> {
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setLocationType(inputDTO.getLocationType());
                        existing.setAddressLine1(inputDTO.getAddressLine1());
                        existing.setAddressLine2(inputDTO.getAddressLine2());
                        existing.setCity(inputDTO.getCity());
                        existing.setStateProvince(inputDTO.getStateProvince());
                        existing.setCountry(inputDTO.getCountry());
                        existing.setPostalCode(inputDTO.getPostalCode());
                        existing.setLatitude(inputDTO.getLatitude());
                        existing.setLongitude(inputDTO.getLongitude());
                        existing.setIsPrimary(inputDTO.getIsPrimary());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionLocation", saved.getLocationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete InstitutionLocation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionLocation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionLocation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_location", id))
            );
    }
    
    /**
     * Delete InstitutionLocation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionLocation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionLocation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_location", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionLocationOutputDTO toOutputDTO(InstitutionLocation entity) {
        return InstitutionLocationOutputDTO.builder()
            .locationId(entity.getLocationId())
            .institutionId(entity.getInstitutionId())
            .locationType(entity.getLocationType())
            .addressLine1(entity.getAddressLine1())
            .addressLine2(entity.getAddressLine2())
            .city(entity.getCity())
            .stateProvince(entity.getStateProvince())
            .country(entity.getCountry())
            .postalCode(entity.getPostalCode())
            .latitude(entity.getLatitude())
            .longitude(entity.getLongitude())
            .isPrimary(entity.getIsPrimary())
            .build();
    }
}