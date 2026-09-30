package com.example.service;

import com.example.entity.JobPostCommunityLink;
import com.example.dto.JobPostCommunityLinkInputDTO;
import com.example.dto.JobPostCommunityLinkOutputDTO;
import com.example.repository.JobPostCommunityLinkRepository;
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
 * Service class for JobPostCommunityLink business logic.
 */
@Service
@RequiredArgsConstructor
public class JobPostCommunityLinkService {
    
    private final JobPostCommunityLinkRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobPostCommunityLink
     */
    @Transactional
    public Mono<JobPostCommunityLinkOutputDTO> create(JobPostCommunityLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobPostCommunityLink entity = JobPostCommunityLink.builder()
                    .jobPostId(inputDTO.getJobPostId())
                    .communityId(inputDTO.getCommunityId())
                    .isFeatured(inputDTO.getIsFeatured())
                    .postedByUserId(inputDTO.getPostedByUserId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_post_community_link")
                            .recordId(saved.getLinkId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostCommunityLink", saved.getLinkId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobPostCommunityLink by ID
     */
    public Mono<JobPostCommunityLinkOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostCommunityLink", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobPostCommunityLinks
     */
    public Flux<JobPostCommunityLinkOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobPostCommunityLinks with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobPostCommunityLinkOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobPostCommunityLink> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_post_community_link", groupIds);
                            Flux<JobPostCommunityLink> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_post_community_link", groupIds, size, offset);
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
     * Update JobPostCommunityLink
     */
    @Transactional
    public Mono<JobPostCommunityLinkOutputDTO> update(Long id, JobPostCommunityLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostCommunityLink", id)))
                    .flatMap(existing -> {
                        existing.setJobPostId(inputDTO.getJobPostId());
                        existing.setCommunityId(inputDTO.getCommunityId());
                        existing.setIsFeatured(inputDTO.getIsFeatured());
                        existing.setPostedByUserId(inputDTO.getPostedByUserId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostCommunityLink", saved.getLinkId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobPostCommunityLink
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostCommunityLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostCommunityLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_community_link", id))
            );
    }
    
    /**
     * Delete JobPostCommunityLink with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostCommunityLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostCommunityLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_community_link", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobPostCommunityLinkOutputDTO toOutputDTO(JobPostCommunityLink entity) {
        return JobPostCommunityLinkOutputDTO.builder()
            .linkId(entity.getLinkId())
            .jobPostId(entity.getJobPostId())
            .communityId(entity.getCommunityId())
            .isFeatured(entity.getIsFeatured())
            .postedByUserId(entity.getPostedByUserId())
            .build();
    }
}