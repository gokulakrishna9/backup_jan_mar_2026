package com.jobportal.service;

import com.jobportal.entity.ExamAnswer;
import com.jobportal.dto.ExamAnswerInputDTO;
import com.jobportal.dto.ExamAnswerOutputDTO;
import com.jobportal.repository.ExamAnswerRepository;
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
 * Service class for ExamAnswer business logic.
 */
@Service
@RequiredArgsConstructor
public class ExamAnswerService {
    
    private final ExamAnswerRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new ExamAnswer
     */
    @Transactional
    public Mono<ExamAnswerOutputDTO> create(ExamAnswerInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                ExamAnswer entity = ExamAnswer.builder()
                    .answertext(inputDTO.getAnswertext())
                    .answercode(inputDTO.getAnswercode())
                    .iscorrect(inputDTO.getIscorrect())
                    .explanation(inputDTO.getExplanation())
                    .sortorder(inputDTO.getSortorder())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("exam_answer")
                            .recordId(saved.getExamAnswerId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "ExamAnswer", saved.getExamAnswerId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find ExamAnswer by ID
     */
    public Mono<ExamAnswerOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("ExamAnswer", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all ExamAnswers
     */
    public Flux<ExamAnswerOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find ExamAnswers with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<ExamAnswerOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<ExamAnswer> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "exam_answer", groupIds);
                            Flux<ExamAnswer> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "exam_answer", groupIds, size, offset);
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
     * Update ExamAnswer
     */
    @Transactional
    public Mono<ExamAnswerOutputDTO> update(Long id, ExamAnswerInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("ExamAnswer", id)))
                    .flatMap(existing -> {
                        existing.setAnswertext(inputDTO.getAnswertext());
                        existing.setAnswercode(inputDTO.getAnswercode());
                        existing.setIscorrect(inputDTO.getIscorrect());
                        existing.setExplanation(inputDTO.getExplanation());
                        existing.setSortorder(inputDTO.getSortorder());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "ExamAnswer", saved.getExamAnswerId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete ExamAnswer
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("ExamAnswer", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "ExamAnswer", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("exam_answer", id))
                    .then()
            );
    }
    
    /**
     * Delete ExamAnswer with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("ExamAnswer", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "ExamAnswer", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("exam_answer", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private ExamAnswerOutputDTO toOutputDTO(ExamAnswer entity) {
        return ExamAnswerOutputDTO.builder()
            .examAnswerId(entity.getExamAnswerId())
            .answertext(entity.getAnswertext())
            .answercode(entity.getAnswercode())
            .iscorrect(entity.getIscorrect())
            .explanation(entity.getExplanation())
            .sortorder(entity.getSortorder())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}