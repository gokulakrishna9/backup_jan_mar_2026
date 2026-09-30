package com.example.service;

import com.example.entity.UserAssignmentSubmission;
import com.example.dto.UserAssignmentSubmissionInputDTO;
import com.example.dto.UserAssignmentSubmissionOutputDTO;
import com.example.repository.UserAssignmentSubmissionRepository;
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
 * Service class for UserAssignmentSubmission business logic.
 */
@Service
@RequiredArgsConstructor
public class UserAssignmentSubmissionService {
    
    private final UserAssignmentSubmissionRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserAssignmentSubmission
     */
    @Transactional
    public Mono<UserAssignmentSubmissionOutputDTO> create(UserAssignmentSubmissionInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserAssignmentSubmission entity = UserAssignmentSubmission.builder()
                    .assignmentId(inputDTO.getAssignmentId())
                    .userId(inputDTO.getUserId())
                    .submissionContent(inputDTO.getSubmissionContent())
                    .submissionFileId(inputDTO.getSubmissionFileId())
                    .submittedAt(inputDTO.getSubmittedAt())
                    .score(inputDTO.getScore())
                    .feedback(inputDTO.getFeedback())
                    .gradedByUserId(inputDTO.getGradedByUserId())
                    .gradedAt(inputDTO.getGradedAt())
                    .status(inputDTO.getStatus())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_assignment_submission")
                            .recordId(saved.getSubmissionId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserAssignmentSubmission", saved.getSubmissionId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserAssignmentSubmission by ID
     */
    public Mono<UserAssignmentSubmissionOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserAssignmentSubmission", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserAssignmentSubmissions
     */
    public Flux<UserAssignmentSubmissionOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserAssignmentSubmissions with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserAssignmentSubmissionOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserAssignmentSubmission> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_assignment_submission", groupIds);
                            Flux<UserAssignmentSubmission> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_assignment_submission", groupIds, size, offset);
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
     * Update UserAssignmentSubmission
     */
    @Transactional
    public Mono<UserAssignmentSubmissionOutputDTO> update(Long id, UserAssignmentSubmissionInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserAssignmentSubmission", id)))
                    .flatMap(existing -> {
                        existing.setAssignmentId(inputDTO.getAssignmentId());
                        existing.setUserId(inputDTO.getUserId());
                        existing.setSubmissionContent(inputDTO.getSubmissionContent());
                        existing.setSubmissionFileId(inputDTO.getSubmissionFileId());
                        existing.setSubmittedAt(inputDTO.getSubmittedAt());
                        existing.setScore(inputDTO.getScore());
                        existing.setFeedback(inputDTO.getFeedback());
                        existing.setGradedByUserId(inputDTO.getGradedByUserId());
                        existing.setGradedAt(inputDTO.getGradedAt());
                        existing.setStatus(inputDTO.getStatus());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserAssignmentSubmission", saved.getSubmissionId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserAssignmentSubmission
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserAssignmentSubmission", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserAssignmentSubmission", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_assignment_submission", id))
            );
    }
    
    /**
     * Delete UserAssignmentSubmission with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserAssignmentSubmission", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserAssignmentSubmission", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_assignment_submission", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserAssignmentSubmissionOutputDTO toOutputDTO(UserAssignmentSubmission entity) {
        return UserAssignmentSubmissionOutputDTO.builder()
            .submissionId(entity.getSubmissionId())
            .assignmentId(entity.getAssignmentId())
            .userId(entity.getUserId())
            .submissionContent(entity.getSubmissionContent())
            .submissionFileId(entity.getSubmissionFileId())
            .submittedAt(entity.getSubmittedAt())
            .score(entity.getScore())
            .feedback(entity.getFeedback())
            .gradedByUserId(entity.getGradedByUserId())
            .gradedAt(entity.getGradedAt())
            .status(entity.getStatus())
            .build();
    }
}