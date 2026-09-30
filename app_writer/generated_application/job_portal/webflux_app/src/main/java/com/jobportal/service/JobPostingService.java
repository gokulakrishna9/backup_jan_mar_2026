package com.jobportal.service;

import com.jobportal.entity.JobPosting;
import com.jobportal.dto.JobPostingInputDTO;
import com.jobportal.dto.JobPostingOutputDTO;
import com.jobportal.repository.JobPostingRepository;
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
 * Service class for JobPosting business logic.
 */
@Service
@RequiredArgsConstructor
public class JobPostingService {
    
    private final JobPostingRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobPosting
     */
    @Transactional
    public Mono<JobPostingOutputDTO> create(JobPostingInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobPosting entity = JobPosting.builder()
                    .title(inputDTO.getTitle())
                    .description(inputDTO.getDescription())
                    .location(inputDTO.getLocation())
                    .salarymin(inputDTO.getSalarymin())
                    .salarymax(inputDTO.getSalarymax())
                    .jobtype(inputDTO.getJobtype())
                    .isactive(inputDTO.getIsactive())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_posting")
                            .recordId(saved.getJobPostingId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPosting", saved.getJobPostingId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobPosting by ID
     */
    public Mono<JobPostingOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPosting", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobPostings
     */
    public Flux<JobPostingOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobPostings with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobPostingOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobPosting> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_posting", groupIds);
                            Flux<JobPosting> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_posting", groupIds, size, offset);
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
     * Update JobPosting
     */
    @Transactional
    public Mono<JobPostingOutputDTO> update(Long id, JobPostingInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPosting", id)))
                    .flatMap(existing -> {
                        existing.setTitle(inputDTO.getTitle());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setLocation(inputDTO.getLocation());
                        existing.setSalarymin(inputDTO.getSalarymin());
                        existing.setSalarymax(inputDTO.getSalarymax());
                        existing.setJobtype(inputDTO.getJobtype());
                        existing.setIsactive(inputDTO.getIsactive());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPosting", saved.getJobPostingId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobPosting
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPosting", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPosting", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_posting", id))
                    .then()
            );
    }
    
    /**
     * Delete JobPosting with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPosting", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPosting", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_posting", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private JobPostingOutputDTO toOutputDTO(JobPosting entity) {
        return JobPostingOutputDTO.builder()
            .jobPostingId(entity.getJobPostingId())
            .title(entity.getTitle())
            .description(entity.getDescription())
            .location(entity.getLocation())
            .salarymin(entity.getSalarymin())
            .salarymax(entity.getSalarymax())
            .jobtype(entity.getJobtype())
            .isactive(entity.getIsactive())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}