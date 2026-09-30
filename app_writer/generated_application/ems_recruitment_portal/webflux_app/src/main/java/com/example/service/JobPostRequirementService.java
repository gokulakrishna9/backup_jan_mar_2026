package com.example.service;

import com.example.entity.JobPostRequirement;
import com.example.dto.JobPostRequirementInputDTO;
import com.example.dto.JobPostRequirementOutputDTO;
import com.example.repository.JobPostRequirementRepository;
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
 * Service class for JobPostRequirement business logic.
 */
@Service
@RequiredArgsConstructor
public class JobPostRequirementService {
    
    private final JobPostRequirementRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobPostRequirement
     */
    @Transactional
    public Mono<JobPostRequirementOutputDTO> create(JobPostRequirementInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobPostRequirement entity = JobPostRequirement.builder()
                    .jobPostId(inputDTO.getJobPostId())
                    .requirementType(inputDTO.getRequirementType())
                    .requirementDescription(inputDTO.getRequirementDescription())
                    .isMandatory(inputDTO.getIsMandatory())
                    .minimumYears(inputDTO.getMinimumYears())
                    .proficiencyLevel(inputDTO.getProficiencyLevel())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_post_requirement")
                            .recordId(saved.getRequirementId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostRequirement", saved.getRequirementId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobPostRequirement by ID
     */
    public Mono<JobPostRequirementOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostRequirement", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobPostRequirements
     */
    public Flux<JobPostRequirementOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobPostRequirements with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobPostRequirementOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobPostRequirement> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_post_requirement", groupIds);
                            Flux<JobPostRequirement> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_post_requirement", groupIds, size, offset);
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
     * Update JobPostRequirement
     */
    @Transactional
    public Mono<JobPostRequirementOutputDTO> update(Long id, JobPostRequirementInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostRequirement", id)))
                    .flatMap(existing -> {
                        existing.setJobPostId(inputDTO.getJobPostId());
                        existing.setRequirementType(inputDTO.getRequirementType());
                        existing.setRequirementDescription(inputDTO.getRequirementDescription());
                        existing.setIsMandatory(inputDTO.getIsMandatory());
                        existing.setMinimumYears(inputDTO.getMinimumYears());
                        existing.setProficiencyLevel(inputDTO.getProficiencyLevel());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostRequirement", saved.getRequirementId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobPostRequirement
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostRequirement", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostRequirement", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_requirement", id))
            );
    }
    
    /**
     * Delete JobPostRequirement with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostRequirement", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostRequirement", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_requirement", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobPostRequirementOutputDTO toOutputDTO(JobPostRequirement entity) {
        return JobPostRequirementOutputDTO.builder()
            .requirementId(entity.getRequirementId())
            .jobPostId(entity.getJobPostId())
            .requirementType(entity.getRequirementType())
            .requirementDescription(entity.getRequirementDescription())
            .isMandatory(entity.getIsMandatory())
            .minimumYears(entity.getMinimumYears())
            .proficiencyLevel(entity.getProficiencyLevel())
            .build();
    }
}