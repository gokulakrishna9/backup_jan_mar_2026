package com.example.service;

import com.example.entity.InstitutionProfileDocument;
import com.example.dto.InstitutionProfileDocumentInputDTO;
import com.example.dto.InstitutionProfileDocumentOutputDTO;
import com.example.repository.InstitutionProfileDocumentRepository;
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
 * Service class for InstitutionProfileDocument business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionProfileDocumentService {
    
    private final InstitutionProfileDocumentRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new InstitutionProfileDocument
     */
    @Transactional
    public Mono<InstitutionProfileDocumentOutputDTO> create(InstitutionProfileDocumentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                InstitutionProfileDocument entity = InstitutionProfileDocument.builder()
                    .institutionId(inputDTO.getInstitutionId())
                    .title(inputDTO.getTitle())
                    .document(inputDTO.getDocument())
                    .documentType(inputDTO.getDocumentType())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("institution_profile_document")
                            .recordId(saved.getDocumentId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionProfileDocument", saved.getDocumentId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find InstitutionProfileDocument by ID
     */
    public Mono<InstitutionProfileDocumentOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionProfileDocument", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all InstitutionProfileDocuments
     */
    public Flux<InstitutionProfileDocumentOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find InstitutionProfileDocuments with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionProfileDocumentOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<InstitutionProfileDocument> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution_profile_document", groupIds);
                            Flux<InstitutionProfileDocument> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution_profile_document", groupIds, size, offset);
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
     * Update InstitutionProfileDocument
     */
    @Transactional
    public Mono<InstitutionProfileDocumentOutputDTO> update(Long id, InstitutionProfileDocumentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionProfileDocument", id)))
                    .flatMap(existing -> {
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setTitle(inputDTO.getTitle());
                        existing.setDocument(inputDTO.getDocument());
                        existing.setDocumentType(inputDTO.getDocumentType());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionProfileDocument", saved.getDocumentId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete InstitutionProfileDocument
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionProfileDocument", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionProfileDocument", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_profile_document", id))
            );
    }
    
    /**
     * Delete InstitutionProfileDocument with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionProfileDocument", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionProfileDocument", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_profile_document", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionProfileDocumentOutputDTO toOutputDTO(InstitutionProfileDocument entity) {
        return InstitutionProfileDocumentOutputDTO.builder()
            .documentId(entity.getDocumentId())
            .institutionId(entity.getInstitutionId())
            .title(entity.getTitle())
            .document(entity.getDocument())
            .documentType(entity.getDocumentType())
            .build();
    }
}