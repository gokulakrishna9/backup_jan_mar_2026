package com.jobportal.service;

import com.jobportal.entity.CourseAnswer;
import com.jobportal.dto.CourseAnswerInputDTO;
import com.jobportal.dto.CourseAnswerOutputDTO;
import com.jobportal.repository.CourseAnswerRepository;
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
 * Service class for CourseAnswer business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseAnswerService {
    
    private final CourseAnswerRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseAnswer
     */
    @Transactional
    public Mono<CourseAnswerOutputDTO> create(CourseAnswerInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseAnswer entity = CourseAnswer.builder()
                    .answertext(inputDTO.getAnswertext())
                    .answercode(inputDTO.getAnswercode())
                    .isaccepted(inputDTO.getIsaccepted())
                    .upvotes(inputDTO.getUpvotes())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_answer")
                            .recordId(saved.getCourseAnswerId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseAnswer", saved.getCourseAnswerId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseAnswer by ID
     */
    public Mono<CourseAnswerOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseAnswer", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseAnswers
     */
    public Flux<CourseAnswerOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseAnswers with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseAnswerOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseAnswer> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_answer", groupIds);
                            Flux<CourseAnswer> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_answer", groupIds, size, offset);
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
     * Update CourseAnswer
     */
    @Transactional
    public Mono<CourseAnswerOutputDTO> update(Long id, CourseAnswerInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseAnswer", id)))
                    .flatMap(existing -> {
                        existing.setAnswertext(inputDTO.getAnswertext());
                        existing.setAnswercode(inputDTO.getAnswercode());
                        existing.setIsaccepted(inputDTO.getIsaccepted());
                        existing.setUpvotes(inputDTO.getUpvotes());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseAnswer", saved.getCourseAnswerId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseAnswer
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseAnswer", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseAnswer", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_answer", id))
                    .then()
            );
    }
    
    /**
     * Delete CourseAnswer with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseAnswer", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseAnswer", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_answer", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private CourseAnswerOutputDTO toOutputDTO(CourseAnswer entity) {
        return CourseAnswerOutputDTO.builder()
            .courseAnswerId(entity.getCourseAnswerId())
            .answertext(entity.getAnswertext())
            .answercode(entity.getAnswercode())
            .isaccepted(entity.getIsaccepted())
            .upvotes(entity.getUpvotes())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}