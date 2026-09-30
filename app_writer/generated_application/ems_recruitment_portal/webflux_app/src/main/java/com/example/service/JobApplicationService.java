package com.example.service;

import com.example.entity.JobApplication;
import com.example.dto.JobApplicationInputDTO;
import com.example.dto.JobApplicationOutputDTO;
import com.example.repository.JobApplicationRepository;
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
 * Service class for JobApplication business logic.
 */
@Service
@RequiredArgsConstructor
public class JobApplicationService {
    
    private final JobApplicationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobApplication
     */
    @Transactional
    public Mono<JobApplicationOutputDTO> create(JobApplicationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobApplication entity = JobApplication.builder()
                    .jobPostId(inputDTO.getJobPostId())
                    .userId(inputDTO.getUserId())
                    .coverLetter(inputDTO.getCoverLetter())
                    .resumeDocumentId(inputDTO.getResumeDocumentId())
                    .applicationStatus(inputDTO.getApplicationStatus())
                    .appliedAt(inputDTO.getAppliedAt())
                    .statusUpdatedAt(inputDTO.getStatusUpdatedAt())
                    .statusUpdatedByUserId(inputDTO.getStatusUpdatedByUserId())
                    .notes(inputDTO.getNotes())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_application")
                            .recordId(saved.getApplicationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobApplication", saved.getApplicationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobApplication by ID
     */
    public Mono<JobApplicationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobApplication", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobApplications
     */
    public Flux<JobApplicationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobApplications with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobApplicationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobApplication> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_application", groupIds);
                            Flux<JobApplication> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_application", groupIds, size, offset);
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
     * Update JobApplication
     */
    @Transactional
    public Mono<JobApplicationOutputDTO> update(Long id, JobApplicationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobApplication", id)))
                    .flatMap(existing -> {
                        existing.setJobPostId(inputDTO.getJobPostId());
                        existing.setUserId(inputDTO.getUserId());
                        existing.setCoverLetter(inputDTO.getCoverLetter());
                        existing.setResumeDocumentId(inputDTO.getResumeDocumentId());
                        existing.setApplicationStatus(inputDTO.getApplicationStatus());
                        existing.setAppliedAt(inputDTO.getAppliedAt());
                        existing.setStatusUpdatedAt(inputDTO.getStatusUpdatedAt());
                        existing.setStatusUpdatedByUserId(inputDTO.getStatusUpdatedByUserId());
                        existing.setNotes(inputDTO.getNotes());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobApplication", saved.getApplicationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobApplication
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobApplication", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobApplication", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_application", id))
            );
    }
    
    /**
     * Delete JobApplication with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobApplication", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobApplication", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_application", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobApplicationOutputDTO toOutputDTO(JobApplication entity) {
        return JobApplicationOutputDTO.builder()
            .applicationId(entity.getApplicationId())
            .jobPostId(entity.getJobPostId())
            .userId(entity.getUserId())
            .coverLetter(entity.getCoverLetter())
            .resumeDocumentId(entity.getResumeDocumentId())
            .applicationStatus(entity.getApplicationStatus())
            .appliedAt(entity.getAppliedAt())
            .statusUpdatedAt(entity.getStatusUpdatedAt())
            .statusUpdatedByUserId(entity.getStatusUpdatedByUserId())
            .notes(entity.getNotes())
            .build();
    }
}