package com.jobportal.service;

import com.jobportal.entity.TrainingCertification;
import com.jobportal.dto.TrainingCertificationInputDTO;
import com.jobportal.dto.TrainingCertificationOutputDTO;
import com.jobportal.repository.TrainingCertificationRepository;
import com.jobportal.exception.EntityNotFoundException;
import com.jobportal.dto.PageResponse;
import com.jobportal.repository.RecordOwnerRepository;
import com.jobportal.repository.QueryGroupRecordRepository;
import com.jobportal.repository.QueryGroupMemberRepository;
import com.jobportal.repository.AuthUserRepository;
import com.jobportal.entity.RecordOwner;
import com.jobportal.security.SecurityContextHolder;
import com.jobportal.auth.JwtService;
import com.jobportal.service.ActivityTrackingService;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Service class for TrainingCertification business logic.
 */
@Service
@RequiredArgsConstructor
public class TrainingCertificationService {
    
    private final TrainingCertificationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new TrainingCertification
     */
    @Transactional
    public Mono<TrainingCertificationOutputDTO> create(TrainingCertificationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                TrainingCertification entity = TrainingCertification.builder()
                    .certificatenumber(inputDTO.getCertificatenumber())
                    .title(inputDTO.getTitle())
                    .issuedat(inputDTO.getIssuedat())
                    .expiresat(inputDTO.getExpiresat())
                    .certificateurl(inputDTO.getCertificateurl())
                    .status(inputDTO.getStatus())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("training_certification")
                            .recordId(saved.getTrainingCertificationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingCertification", saved.getTrainingCertificationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find TrainingCertification by ID
     */
    public Mono<TrainingCertificationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingCertification", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all TrainingCertifications
     */
    public Flux<TrainingCertificationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find TrainingCertifications with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<TrainingCertificationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<TrainingCertification> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "training_certification", groupIds);
                            Flux<TrainingCertification> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "training_certification", groupIds, size, offset);
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
     * Update TrainingCertification
     */
    @Transactional
    public Mono<TrainingCertificationOutputDTO> update(Long id, TrainingCertificationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingCertification", id)))
                    .flatMap(existing -> {
                        existing.setCertificatenumber(inputDTO.getCertificatenumber());
                        existing.setTitle(inputDTO.getTitle());
                        existing.setIssuedat(inputDTO.getIssuedat());
                        existing.setExpiresat(inputDTO.getExpiresat());
                        existing.setCertificateurl(inputDTO.getCertificateurl());
                        existing.setStatus(inputDTO.getStatus());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingCertification", saved.getTrainingCertificationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete TrainingCertification
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingCertification", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingCertification", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("training_certification", id))
                    .then()
            );
    }
    
    /**
     * Delete TrainingCertification with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingCertification", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingCertification", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("training_certification", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private TrainingCertificationOutputDTO toOutputDTO(TrainingCertification entity) {
        return TrainingCertificationOutputDTO.builder()
            .trainingCertificationId(entity.getTrainingCertificationId())
            .certificatenumber(entity.getCertificatenumber())
            .title(entity.getTitle())
            .issuedat(entity.getIssuedat())
            .expiresat(entity.getExpiresat())
            .certificateurl(entity.getCertificateurl())
            .status(entity.getStatus())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}