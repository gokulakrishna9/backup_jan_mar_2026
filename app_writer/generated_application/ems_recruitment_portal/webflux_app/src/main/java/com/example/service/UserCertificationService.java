package com.example.service;

import com.example.entity.UserCertification;
import com.example.dto.UserCertificationInputDTO;
import com.example.dto.UserCertificationOutputDTO;
import com.example.repository.UserCertificationRepository;
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
 * Service class for UserCertification business logic.
 */
@Service
@RequiredArgsConstructor
public class UserCertificationService {
    
    private final UserCertificationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserCertification
     */
    @Transactional
    public Mono<UserCertificationOutputDTO> create(UserCertificationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserCertification entity = UserCertification.builder()
                    .userId(inputDTO.getUserId())
                    .certificationName(inputDTO.getCertificationName())
                    .issuingOrganization(inputDTO.getIssuingOrganization())
                    .institutionId(inputDTO.getInstitutionId())
                    .issueDate(inputDTO.getIssueDate())
                    .expiryDate(inputDTO.getExpiryDate())
                    .credentialId(inputDTO.getCredentialId())
                    .credentialUrl(inputDTO.getCredentialUrl())
                    .certificateDocumentId(inputDTO.getCertificateDocumentId())
                    .isVerified(inputDTO.getIsVerified())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_certification")
                            .recordId(saved.getCertificationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCertification", saved.getCertificationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserCertification by ID
     */
    public Mono<UserCertificationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCertification", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserCertifications
     */
    public Flux<UserCertificationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserCertifications with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserCertificationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserCertification> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_certification", groupIds);
                            Flux<UserCertification> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_certification", groupIds, size, offset);
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
     * Update UserCertification
     */
    @Transactional
    public Mono<UserCertificationOutputDTO> update(Long id, UserCertificationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCertification", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setCertificationName(inputDTO.getCertificationName());
                        existing.setIssuingOrganization(inputDTO.getIssuingOrganization());
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setIssueDate(inputDTO.getIssueDate());
                        existing.setExpiryDate(inputDTO.getExpiryDate());
                        existing.setCredentialId(inputDTO.getCredentialId());
                        existing.setCredentialUrl(inputDTO.getCredentialUrl());
                        existing.setCertificateDocumentId(inputDTO.getCertificateDocumentId());
                        existing.setIsVerified(inputDTO.getIsVerified());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCertification", saved.getCertificationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserCertification
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCertification", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCertification", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_certification", id))
            );
    }
    
    /**
     * Delete UserCertification with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCertification", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCertification", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_certification", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserCertificationOutputDTO toOutputDTO(UserCertification entity) {
        return UserCertificationOutputDTO.builder()
            .certificationId(entity.getCertificationId())
            .userId(entity.getUserId())
            .certificationName(entity.getCertificationName())
            .issuingOrganization(entity.getIssuingOrganization())
            .institutionId(entity.getInstitutionId())
            .issueDate(entity.getIssueDate())
            .expiryDate(entity.getExpiryDate())
            .credentialId(entity.getCredentialId())
            .credentialUrl(entity.getCredentialUrl())
            .certificateDocumentId(entity.getCertificateDocumentId())
            .isVerified(entity.getIsVerified())
            .build();
    }
}