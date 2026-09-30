package com.jobportal.service;

import com.jobportal.entity.TrainingEnrollment;
import com.jobportal.dto.TrainingEnrollmentInputDTO;
import com.jobportal.dto.TrainingEnrollmentOutputDTO;
import com.jobportal.repository.TrainingEnrollmentRepository;
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
 * Service class for TrainingEnrollment business logic.
 */
@Service
@RequiredArgsConstructor
public class TrainingEnrollmentService {
    
    private final TrainingEnrollmentRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new TrainingEnrollment
     */
    @Transactional
    public Mono<TrainingEnrollmentOutputDTO> create(TrainingEnrollmentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                TrainingEnrollment entity = TrainingEnrollment.builder()
                    .status(inputDTO.getStatus())
                    .progress(inputDTO.getProgress())
                    .enrolledat(inputDTO.getEnrolledat())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("training_enrollment")
                            .recordId(saved.getTrainingEnrollmentId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingEnrollment", saved.getTrainingEnrollmentId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find TrainingEnrollment by ID
     */
    public Mono<TrainingEnrollmentOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingEnrollment", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all TrainingEnrollments
     */
    public Flux<TrainingEnrollmentOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find TrainingEnrollments with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<TrainingEnrollmentOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<TrainingEnrollment> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "training_enrollment", groupIds);
                            Flux<TrainingEnrollment> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "training_enrollment", groupIds, size, offset);
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
     * Update TrainingEnrollment
     */
    @Transactional
    public Mono<TrainingEnrollmentOutputDTO> update(Long id, TrainingEnrollmentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingEnrollment", id)))
                    .flatMap(existing -> {
                        existing.setStatus(inputDTO.getStatus());
                        existing.setProgress(inputDTO.getProgress());
                        existing.setEnrolledat(inputDTO.getEnrolledat());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingEnrollment", saved.getTrainingEnrollmentId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete TrainingEnrollment
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingEnrollment", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingEnrollment", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("training_enrollment", id))
                    .then()
            );
    }
    
    /**
     * Delete TrainingEnrollment with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingEnrollment", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingEnrollment", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("training_enrollment", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private TrainingEnrollmentOutputDTO toOutputDTO(TrainingEnrollment entity) {
        return TrainingEnrollmentOutputDTO.builder()
            .trainingEnrollmentId(entity.getTrainingEnrollmentId())
            .status(entity.getStatus())
            .progress(entity.getProgress())
            .enrolledat(entity.getEnrolledat())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}