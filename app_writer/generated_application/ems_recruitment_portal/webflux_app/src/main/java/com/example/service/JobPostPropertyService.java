package com.example.service;

import com.example.entity.JobPostProperty;
import com.example.dto.JobPostPropertyInputDTO;
import com.example.dto.JobPostPropertyOutputDTO;
import com.example.repository.JobPostPropertyRepository;
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
 * Service class for JobPostProperty business logic.
 */
@Service
@RequiredArgsConstructor
public class JobPostPropertyService {
    
    private final JobPostPropertyRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobPostProperty
     */
    @Transactional
    public Mono<JobPostPropertyOutputDTO> create(JobPostPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobPostProperty entity = JobPostProperty.builder()
                    .propertyName(inputDTO.getPropertyName())
                    .propertyValue(inputDTO.getPropertyValue())
                    .propertyType(inputDTO.getPropertyType())
                    .propertyDescription(inputDTO.getPropertyDescription())
                    .groupId(inputDTO.getGroupId())
                    .jobPostId(inputDTO.getJobPostId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_post_property")
                            .recordId(saved.getPropertyId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostProperty", saved.getPropertyId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobPostProperty by ID
     */
    public Mono<JobPostPropertyOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostProperty", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobPostPropertys
     */
    public Flux<JobPostPropertyOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobPostPropertys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobPostPropertyOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobPostProperty> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_post_property", groupIds);
                            Flux<JobPostProperty> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_post_property", groupIds, size, offset);
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
     * Update JobPostProperty
     */
    @Transactional
    public Mono<JobPostPropertyOutputDTO> update(Long id, JobPostPropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostProperty", id)))
                    .flatMap(existing -> {
                        existing.setPropertyName(inputDTO.getPropertyName());
                        existing.setPropertyValue(inputDTO.getPropertyValue());
                        existing.setPropertyType(inputDTO.getPropertyType());
                        existing.setPropertyDescription(inputDTO.getPropertyDescription());
                        existing.setGroupId(inputDTO.getGroupId());
                        existing.setJobPostId(inputDTO.getJobPostId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostProperty", saved.getPropertyId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobPostProperty
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_property", id))
            );
    }
    
    /**
     * Delete JobPostProperty with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_property", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobPostPropertyOutputDTO toOutputDTO(JobPostProperty entity) {
        return JobPostPropertyOutputDTO.builder()
            .propertyId(entity.getPropertyId())
            .propertyName(entity.getPropertyName())
            .propertyValue(entity.getPropertyValue())
            .propertyType(entity.getPropertyType())
            .propertyDescription(entity.getPropertyDescription())
            .groupId(entity.getGroupId())
            .jobPostId(entity.getJobPostId())
            .build();
    }
}