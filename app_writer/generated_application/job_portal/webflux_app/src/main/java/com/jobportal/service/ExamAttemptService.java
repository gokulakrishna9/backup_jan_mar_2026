package com.jobportal.service;

import com.jobportal.entity.ExamAttempt;
import com.jobportal.dto.ExamAttemptInputDTO;
import com.jobportal.dto.ExamAttemptOutputDTO;
import com.jobportal.repository.ExamAttemptRepository;
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
 * Service class for ExamAttempt business logic.
 */
@Service
@RequiredArgsConstructor
public class ExamAttemptService {
    
    private final ExamAttemptRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new ExamAttempt
     */
    @Transactional
    public Mono<ExamAttemptOutputDTO> create(ExamAttemptInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                ExamAttempt entity = ExamAttempt.builder()
                    .score(inputDTO.getScore())
                    .passed(inputDTO.getPassed())
                    .startedat(inputDTO.getStartedat())
                    .completedat(inputDTO.getCompletedat())
                    .attemptnumber(inputDTO.getAttemptnumber())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("exam_attempt")
                            .recordId(saved.getExamAttemptId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "ExamAttempt", saved.getExamAttemptId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find ExamAttempt by ID
     */
    public Mono<ExamAttemptOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("ExamAttempt", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all ExamAttempts
     */
    public Flux<ExamAttemptOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find ExamAttempts with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<ExamAttemptOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<ExamAttempt> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "exam_attempt", groupIds);
                            Flux<ExamAttempt> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "exam_attempt", groupIds, size, offset);
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
     * Update ExamAttempt
     */
    @Transactional
    public Mono<ExamAttemptOutputDTO> update(Long id, ExamAttemptInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("ExamAttempt", id)))
                    .flatMap(existing -> {
                        existing.setScore(inputDTO.getScore());
                        existing.setPassed(inputDTO.getPassed());
                        existing.setStartedat(inputDTO.getStartedat());
                        existing.setCompletedat(inputDTO.getCompletedat());
                        existing.setAttemptnumber(inputDTO.getAttemptnumber());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "ExamAttempt", saved.getExamAttemptId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete ExamAttempt
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("ExamAttempt", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "ExamAttempt", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("exam_attempt", id))
                    .then()
            );
    }
    
    /**
     * Delete ExamAttempt with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("ExamAttempt", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "ExamAttempt", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("exam_attempt", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private ExamAttemptOutputDTO toOutputDTO(ExamAttempt entity) {
        return ExamAttemptOutputDTO.builder()
            .examAttemptId(entity.getExamAttemptId())
            .score(entity.getScore())
            .passed(entity.getPassed())
            .startedat(entity.getStartedat())
            .completedat(entity.getCompletedat())
            .attemptnumber(entity.getAttemptnumber())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}