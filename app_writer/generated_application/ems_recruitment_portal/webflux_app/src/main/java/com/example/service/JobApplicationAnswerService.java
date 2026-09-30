package com.example.service;

import com.example.entity.JobApplicationAnswer;
import com.example.dto.JobApplicationAnswerInputDTO;
import com.example.dto.JobApplicationAnswerOutputDTO;
import com.example.repository.JobApplicationAnswerRepository;
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
 * Service class for JobApplicationAnswer business logic.
 */
@Service
@RequiredArgsConstructor
public class JobApplicationAnswerService {
    
    private final JobApplicationAnswerRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new JobApplicationAnswer
     */
    @Transactional
    public Mono<JobApplicationAnswerOutputDTO> create(JobApplicationAnswerInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                JobApplicationAnswer entity = JobApplicationAnswer.builder()
                    .applicationId(inputDTO.getApplicationId())
                    .questionId(inputDTO.getQuestionId())
                    .answerText(inputDTO.getAnswerText())
                    .answerFileId(inputDTO.getAnswerFileId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("job_application_answer")
                            .recordId(saved.getAnswerId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobApplicationAnswer", saved.getAnswerId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find JobApplicationAnswer by ID
     */
    public Mono<JobApplicationAnswerOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("JobApplicationAnswer", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all JobApplicationAnswers
     */
    public Flux<JobApplicationAnswerOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find JobApplicationAnswers with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<JobApplicationAnswerOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<JobApplicationAnswer> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "job_application_answer", groupIds);
                            Flux<JobApplicationAnswer> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "job_application_answer", groupIds, size, offset);
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
     * Update JobApplicationAnswer
     */
    @Transactional
    public Mono<JobApplicationAnswerOutputDTO> update(Long id, JobApplicationAnswerInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobApplicationAnswer", id)))
                    .flatMap(existing -> {
                        existing.setApplicationId(inputDTO.getApplicationId());
                        existing.setQuestionId(inputDTO.getQuestionId());
                        existing.setAnswerText(inputDTO.getAnswerText());
                        existing.setAnswerFileId(inputDTO.getAnswerFileId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "JobApplicationAnswer", saved.getAnswerId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete JobApplicationAnswer
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobApplicationAnswer", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobApplicationAnswer", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_application_answer", id))
            );
    }
    
    /**
     * Delete JobApplicationAnswer with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("JobApplicationAnswer", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "JobApplicationAnswer", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("job_application_answer", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private JobApplicationAnswerOutputDTO toOutputDTO(JobApplicationAnswer entity) {
        return JobApplicationAnswerOutputDTO.builder()
            .answerId(entity.getAnswerId())
            .applicationId(entity.getApplicationId())
            .questionId(entity.getQuestionId())
            .answerText(entity.getAnswerText())
            .answerFileId(entity.getAnswerFileId())
            .build();
    }
}