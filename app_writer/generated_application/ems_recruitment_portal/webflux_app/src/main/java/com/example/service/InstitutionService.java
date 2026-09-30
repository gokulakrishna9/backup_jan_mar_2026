package com.example.service;

import com.example.entity.Institution;
import com.example.dto.InstitutionInputDTO;
import com.example.dto.InstitutionOutputDTO;
import com.example.repository.InstitutionRepository;
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
 * Service class for Institution business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionService {
    
    private final InstitutionRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new Institution
     */
    @Transactional
    public Mono<InstitutionOutputDTO> create(InstitutionInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                Institution entity = Institution.builder()
                    .name(inputDTO.getName())
                    .description(inputDTO.getDescription())
                    .moto(inputDTO.getMoto())
                    .institutionTypeId(inputDTO.getInstitutionTypeId())
                    .website(inputDTO.getWebsite())
                    .contactEmail(inputDTO.getContactEmail())
                    .contactPhone(inputDTO.getContactPhone())
                    .isActive(inputDTO.getIsActive())
                    .isEntity(inputDTO.getIsEntity())
                    .isPublic(inputDTO.getIsPublic())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("institution")
                            .recordId(saved.getInstitutionId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "Institution", saved.getInstitutionId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find Institution by ID
     */
    public Mono<InstitutionOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("Institution", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all Institutions
     */
    public Flux<InstitutionOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find Institutions with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<Institution> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution", groupIds);
                            Flux<Institution> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution", groupIds, size, offset);
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
     * Update Institution
     */
    @Transactional
    public Mono<InstitutionOutputDTO> update(Long id, InstitutionInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Institution", id)))
                    .flatMap(existing -> {
                        existing.setName(inputDTO.getName());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setMoto(inputDTO.getMoto());
                        existing.setInstitutionTypeId(inputDTO.getInstitutionTypeId());
                        existing.setWebsite(inputDTO.getWebsite());
                        existing.setContactEmail(inputDTO.getContactEmail());
                        existing.setContactPhone(inputDTO.getContactPhone());
                        existing.setIsActive(inputDTO.getIsActive());
                        existing.setIsEntity(inputDTO.getIsEntity());
                        existing.setIsPublic(inputDTO.getIsPublic());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "Institution", saved.getInstitutionId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete Institution
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Institution", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Institution", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution", id))
            );
    }
    
    /**
     * Delete Institution with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Institution", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Institution", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionOutputDTO toOutputDTO(Institution entity) {
        return InstitutionOutputDTO.builder()
            .institutionId(entity.getInstitutionId())
            .name(entity.getName())
            .description(entity.getDescription())
            .moto(entity.getMoto())
            .institutionTypeId(entity.getInstitutionTypeId())
            .website(entity.getWebsite())
            .contactEmail(entity.getContactEmail())
            .contactPhone(entity.getContactPhone())
            .isActive(entity.getIsActive())
            .isEntity(entity.getIsEntity())
            .isPublic(entity.getIsPublic())
            .build();
    }
}