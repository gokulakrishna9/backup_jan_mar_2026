package com.example.service;

import com.example.entity.JobPost;
import com.example.dto.JobPostInputDTO;
import com.example.dto.JobPostOutputDTO;
import com.example.repository.JobPostRepository;
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
 * Service class for JobPost business logic.
 */
@Service
@RequiredArgsConstructor
public class JobPostService {
    
    private final JobPostRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobPost
     */
    @Transactional
    public Mono<JobPostOutputDTO> create(JobPostInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobPost entity = JobPost.builder()
                    .jobPostSubject(inputDTO.getJobPostSubject())
                    .jobPostDescription(inputDTO.getJobPostDescription())
                    .institutionId(inputDTO.getInstitutionId())
                    .location(inputDTO.getLocation())
                    .salaryRange(inputDTO.getSalaryRange())
                    .postedOn(inputDTO.getPostedOn())
                    .expiresOn(inputDTO.getExpiresOn())
                    .isActive(inputDTO.getIsActive())
                    .isEntity(inputDTO.getIsEntity())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_post")
                            .recordId(saved.getJobPostId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPost", saved.getJobPostId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobPost by ID
     */
    public Mono<JobPostOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPost", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobPosts
     */
    public Flux<JobPostOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobPosts with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobPostOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobPost> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_post", groupIds);
                            Flux<JobPost> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_post", groupIds, size, offset);
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
     * Update JobPost
     */
    @Transactional
    public Mono<JobPostOutputDTO> update(Long id, JobPostInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPost", id)))
                    .flatMap(existing -> {
                        existing.setJobPostSubject(inputDTO.getJobPostSubject());
                        existing.setJobPostDescription(inputDTO.getJobPostDescription());
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setLocation(inputDTO.getLocation());
                        existing.setSalaryRange(inputDTO.getSalaryRange());
                        existing.setPostedOn(inputDTO.getPostedOn());
                        existing.setExpiresOn(inputDTO.getExpiresOn());
                        existing.setIsActive(inputDTO.getIsActive());
                        existing.setIsEntity(inputDTO.getIsEntity());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPost", saved.getJobPostId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobPost
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPost", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPost", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post", id))
            );
    }
    
    /**
     * Delete JobPost with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPost", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPost", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobPostOutputDTO toOutputDTO(JobPost entity) {
        return JobPostOutputDTO.builder()
            .jobPostId(entity.getJobPostId())
            .jobPostSubject(entity.getJobPostSubject())
            .jobPostDescription(entity.getJobPostDescription())
            .institutionId(entity.getInstitutionId())
            .location(entity.getLocation())
            .salaryRange(entity.getSalaryRange())
            .postedOn(entity.getPostedOn())
            .expiresOn(entity.getExpiresOn())
            .isActive(entity.getIsActive())
            .isEntity(entity.getIsEntity())
            .build();
    }
}