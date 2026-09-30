package com.example.service;

import com.example.entity.UserProfileDocument;
import com.example.dto.UserProfileDocumentInputDTO;
import com.example.dto.UserProfileDocumentOutputDTO;
import com.example.repository.UserProfileDocumentRepository;
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
 * Service class for UserProfileDocument business logic.
 */
@Service
@RequiredArgsConstructor
public class UserProfileDocumentService {
    
    private final UserProfileDocumentRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserProfileDocument
     */
    @Transactional
    public Mono<UserProfileDocumentOutputDTO> create(UserProfileDocumentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserProfileDocument entity = UserProfileDocument.builder()
                    .userId(inputDTO.getUserId())
                    .title(inputDTO.getTitle())
                    .document(inputDTO.getDocument())
                    .documentType(inputDTO.getDocumentType())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_profile_document")
                            .recordId(saved.getDocumentId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProfileDocument", saved.getDocumentId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserProfileDocument by ID
     */
    public Mono<UserProfileDocumentOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProfileDocument", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserProfileDocuments
     */
    public Flux<UserProfileDocumentOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserProfileDocuments with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserProfileDocumentOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserProfileDocument> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_profile_document", groupIds);
                            Flux<UserProfileDocument> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_profile_document", groupIds, size, offset);
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
     * Update UserProfileDocument
     */
    @Transactional
    public Mono<UserProfileDocumentOutputDTO> update(Long id, UserProfileDocumentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProfileDocument", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setTitle(inputDTO.getTitle());
                        existing.setDocument(inputDTO.getDocument());
                        existing.setDocumentType(inputDTO.getDocumentType());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProfileDocument", saved.getDocumentId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserProfileDocument
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProfileDocument", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProfileDocument", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_profile_document", id))
            );
    }
    
    /**
     * Delete UserProfileDocument with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProfileDocument", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProfileDocument", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_profile_document", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserProfileDocumentOutputDTO toOutputDTO(UserProfileDocument entity) {
        return UserProfileDocumentOutputDTO.builder()
            .documentId(entity.getDocumentId())
            .userId(entity.getUserId())
            .title(entity.getTitle())
            .document(entity.getDocument())
            .documentType(entity.getDocumentType())
            .build();
    }
}