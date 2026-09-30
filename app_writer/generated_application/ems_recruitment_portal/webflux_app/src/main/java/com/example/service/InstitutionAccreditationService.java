package com.example.service;

import com.example.entity.InstitutionAccreditation;
import com.example.dto.InstitutionAccreditationInputDTO;
import com.example.dto.InstitutionAccreditationOutputDTO;
import com.example.repository.InstitutionAccreditationRepository;
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
 * Service class for InstitutionAccreditation business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionAccreditationService {
    
    private final InstitutionAccreditationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new InstitutionAccreditation
     */
    @Transactional
    public Mono<InstitutionAccreditationOutputDTO> create(InstitutionAccreditationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                InstitutionAccreditation entity = InstitutionAccreditation.builder()
                    .institutionId(inputDTO.getInstitutionId())
                    .accreditingBody(inputDTO.getAccreditingBody())
                    .accreditationType(inputDTO.getAccreditationType())
                    .accreditationLevel(inputDTO.getAccreditationLevel())
                    .issueDate(inputDTO.getIssueDate())
                    .expiryDate(inputDTO.getExpiryDate())
                    .certificateDocumentId(inputDTO.getCertificateDocumentId())
                    .isActive(inputDTO.getIsActive())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("institution_accreditation")
                            .recordId(saved.getAccreditationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionAccreditation", saved.getAccreditationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find InstitutionAccreditation by ID
     */
    public Mono<InstitutionAccreditationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionAccreditation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all InstitutionAccreditations
     */
    public Flux<InstitutionAccreditationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find InstitutionAccreditations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionAccreditationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<InstitutionAccreditation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution_accreditation", groupIds);
                            Flux<InstitutionAccreditation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution_accreditation", groupIds, size, offset);
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
     * Update InstitutionAccreditation
     */
    @Transactional
    public Mono<InstitutionAccreditationOutputDTO> update(Long id, InstitutionAccreditationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionAccreditation", id)))
                    .flatMap(existing -> {
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setAccreditingBody(inputDTO.getAccreditingBody());
                        existing.setAccreditationType(inputDTO.getAccreditationType());
                        existing.setAccreditationLevel(inputDTO.getAccreditationLevel());
                        existing.setIssueDate(inputDTO.getIssueDate());
                        existing.setExpiryDate(inputDTO.getExpiryDate());
                        existing.setCertificateDocumentId(inputDTO.getCertificateDocumentId());
                        existing.setIsActive(inputDTO.getIsActive());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionAccreditation", saved.getAccreditationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete InstitutionAccreditation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionAccreditation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionAccreditation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_accreditation", id))
            );
    }
    
    /**
     * Delete InstitutionAccreditation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionAccreditation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionAccreditation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_accreditation", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionAccreditationOutputDTO toOutputDTO(InstitutionAccreditation entity) {
        return InstitutionAccreditationOutputDTO.builder()
            .accreditationId(entity.getAccreditationId())
            .institutionId(entity.getInstitutionId())
            .accreditingBody(entity.getAccreditingBody())
            .accreditationType(entity.getAccreditationType())
            .accreditationLevel(entity.getAccreditationLevel())
            .issueDate(entity.getIssueDate())
            .expiryDate(entity.getExpiryDate())
            .certificateDocumentId(entity.getCertificateDocumentId())
            .isActive(entity.getIsActive())
            .build();
    }
}