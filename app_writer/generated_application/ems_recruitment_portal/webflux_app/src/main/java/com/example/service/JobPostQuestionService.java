package com.example.service;

import com.example.entity.JobPostQuestion;
import com.example.dto.JobPostQuestionInputDTO;
import com.example.dto.JobPostQuestionOutputDTO;
import com.example.repository.JobPostQuestionRepository;
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
 * Service class for JobPostQuestion business logic.
 */
@Service
@RequiredArgsConstructor
public class JobPostQuestionService {
    
    private final JobPostQuestionRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobPostQuestion
     */
    @Transactional
    public Mono<JobPostQuestionOutputDTO> create(JobPostQuestionInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobPostQuestion entity = JobPostQuestion.builder()
                    .jobPostId(inputDTO.getJobPostId())
                    .questionText(inputDTO.getQuestionText())
                    .questionType(inputDTO.getQuestionType())
                    .isRequired(inputDTO.getIsRequired())
                    .orderSequence(inputDTO.getOrderSequence())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_post_question")
                            .recordId(saved.getQuestionId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostQuestion", saved.getQuestionId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobPostQuestion by ID
     */
    public Mono<JobPostQuestionOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostQuestion", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobPostQuestions
     */
    public Flux<JobPostQuestionOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobPostQuestions with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobPostQuestionOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobPostQuestion> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_post_question", groupIds);
                            Flux<JobPostQuestion> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_post_question", groupIds, size, offset);
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
     * Update JobPostQuestion
     */
    @Transactional
    public Mono<JobPostQuestionOutputDTO> update(Long id, JobPostQuestionInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostQuestion", id)))
                    .flatMap(existing -> {
                        existing.setJobPostId(inputDTO.getJobPostId());
                        existing.setQuestionText(inputDTO.getQuestionText());
                        existing.setQuestionType(inputDTO.getQuestionType());
                        existing.setIsRequired(inputDTO.getIsRequired());
                        existing.setOrderSequence(inputDTO.getOrderSequence());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostQuestion", saved.getQuestionId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobPostQuestion
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostQuestion", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostQuestion", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_question", id))
            );
    }
    
    /**
     * Delete JobPostQuestion with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobPostQuestion", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobPostQuestion", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_post_question", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobPostQuestionOutputDTO toOutputDTO(JobPostQuestion entity) {
        return JobPostQuestionOutputDTO.builder()
            .questionId(entity.getQuestionId())
            .jobPostId(entity.getJobPostId())
            .questionText(entity.getQuestionText())
            .questionType(entity.getQuestionType())
            .isRequired(entity.getIsRequired())
            .orderSequence(entity.getOrderSequence())
            .build();
    }
}