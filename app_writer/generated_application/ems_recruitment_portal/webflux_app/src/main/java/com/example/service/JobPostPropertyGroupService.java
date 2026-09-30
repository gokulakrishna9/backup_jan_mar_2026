package com.example.service;

import com.example.entity.JobPostPropertyGroup;
import com.example.dto.JobPostPropertyGroupInputDTO;
import com.example.dto.JobPostPropertyGroupOutputDTO;
import com.example.repository.JobPostPropertyGroupRepository;
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
 * Service class for JobPostPropertyGroup business logic.
 */
@Service
@RequiredArgsConstructor
public class JobPostPropertyGroupService {
    
    private final JobPostPropertyGroupRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobPostPropertyGroup
     */
    @Transactional
    public Mono<JobPostPropertyGroupOutputDTO> create(JobPostPropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobPostPropertyGroup entity = JobPostPropertyGroup.builder()
                    .groupName(inputDTO.getGroupName())
                    .groupDescription(inputDTO.getGroupDescription())
                    .jobPostId(inputDTO.getJobPostId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_post_property_group")
                            .recordId(saved.getGroupId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostPropertyGroup", saved.getGroupId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobPostPropertyGroup by ID
     */
    public Mono<JobPostPropertyGroupOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostPropertyGroup", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobPostPropertyGroups
     */
    public Flux<JobPostPropertyGroupOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobPostPropertyGroups with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobPostPropertyGroupOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobPostPropertyGroup> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_post_property_group", groupIds);
                            Flux<JobPostPropertyGroup> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_post_property_group", groupIds, size, offset);
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
     * Update JobPostPropertyGroup
     */
    @Transactional
    public Mono<JobPostPropertyGroupOutputDTO> update(Long id, JobPostPropertyGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostPropertyGroup", id)))
                    .flatMap(existing -> {
                        existing.setGroupName(inputDTO.getGroupName());
                        existing.setGroupDescription(inputDTO.getGroupDescription());
                        existing.setJobPostId(inputDTO.getJobPostId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostPropertyGroup", saved.getGroupId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobPostPropertyGroup
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostPropertyGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostPropertyGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_property_group", id))
            );
    }
    
    /**
     * Delete JobPostPropertyGroup with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostPropertyGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostPropertyGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_property_group", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobPostPropertyGroupOutputDTO toOutputDTO(JobPostPropertyGroup entity) {
        return JobPostPropertyGroupOutputDTO.builder()
            .groupId(entity.getGroupId())
            .groupName(entity.getGroupName())
            .groupDescription(entity.getGroupDescription())
            .jobPostId(entity.getJobPostId())
            .build();
    }
}