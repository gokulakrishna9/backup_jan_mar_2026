package com.example.service;

import com.example.entity.JobInterview;
import com.example.dto.JobInterviewInputDTO;
import com.example.dto.JobInterviewOutputDTO;
import com.example.repository.JobInterviewRepository;
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
 * Service class for JobInterview business logic.
 */
@Service
@RequiredArgsConstructor
public class JobInterviewService {
    
    private final JobInterviewRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobInterview
     */
    @Transactional
    public Mono<JobInterviewOutputDTO> create(JobInterviewInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobInterview entity = JobInterview.builder()
                    .applicationId(inputDTO.getApplicationId())
                    .interviewType(inputDTO.getInterviewType())
                    .interviewRound(inputDTO.getInterviewRound())
                    .scheduledAt(inputDTO.getScheduledAt())
                    .durationMinutes(inputDTO.getDurationMinutes())
                    .location(inputDTO.getLocation())
                    .meetingLink(inputDTO.getMeetingLink())
                    .interviewerUserId(inputDTO.getInterviewerUserId())
                    .status(inputDTO.getStatus())
                    .feedback(inputDTO.getFeedback())
                    .rating(inputDTO.getRating())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_interview")
                            .recordId(saved.getInterviewId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobInterview", saved.getInterviewId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobInterview by ID
     */
    public Mono<JobInterviewOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobInterview", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobInterviews
     */
    public Flux<JobInterviewOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobInterviews with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobInterviewOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobInterview> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_interview", groupIds);
                            Flux<JobInterview> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_interview", groupIds, size, offset);
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
     * Update JobInterview
     */
    @Transactional
    public Mono<JobInterviewOutputDTO> update(Long id, JobInterviewInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobInterview", id)))
                    .flatMap(existing -> {
                        existing.setApplicationId(inputDTO.getApplicationId());
                        existing.setInterviewType(inputDTO.getInterviewType());
                        existing.setInterviewRound(inputDTO.getInterviewRound());
                        existing.setScheduledAt(inputDTO.getScheduledAt());
                        existing.setDurationMinutes(inputDTO.getDurationMinutes());
                        existing.setLocation(inputDTO.getLocation());
                        existing.setMeetingLink(inputDTO.getMeetingLink());
                        existing.setInterviewerUserId(inputDTO.getInterviewerUserId());
                        existing.setStatus(inputDTO.getStatus());
                        existing.setFeedback(inputDTO.getFeedback());
                        existing.setRating(inputDTO.getRating());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobInterview", saved.getInterviewId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobInterview
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobInterview", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobInterview", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_interview", id))
            );
    }
    
    /**
     * Delete JobInterview with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobInterview", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobInterview", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_interview", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobInterviewOutputDTO toOutputDTO(JobInterview entity) {
        return JobInterviewOutputDTO.builder()
            .interviewId(entity.getInterviewId())
            .applicationId(entity.getApplicationId())
            .interviewType(entity.getInterviewType())
            .interviewRound(entity.getInterviewRound())
            .scheduledAt(entity.getScheduledAt())
            .durationMinutes(entity.getDurationMinutes())
            .location(entity.getLocation())
            .meetingLink(entity.getMeetingLink())
            .interviewerUserId(entity.getInterviewerUserId())
            .status(entity.getStatus())
            .feedback(entity.getFeedback())
            .rating(entity.getRating())
            .build();
    }
}