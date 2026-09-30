package com.example.service;

import com.example.entity.UserCourseProgress;
import com.example.dto.UserCourseProgressInputDTO;
import com.example.dto.UserCourseProgressOutputDTO;
import com.example.repository.UserCourseProgressRepository;
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
 * Service class for UserCourseProgress business logic.
 */
@Service
@RequiredArgsConstructor
public class UserCourseProgressService {
    
    private final UserCourseProgressRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserCourseProgress
     */
    @Transactional
    public Mono<UserCourseProgressOutputDTO> create(UserCourseProgressInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserCourseProgress entity = UserCourseProgress.builder()
                    .userId(inputDTO.getUserId())
                    .courseId(inputDTO.getCourseId())
                    .lessonId(inputDTO.getLessonId())
                    .completionPercentage(inputDTO.getCompletionPercentage())
                    .lastAccessedAt(inputDTO.getLastAccessedAt())
                    .timeSpentMinutes(inputDTO.getTimeSpentMinutes())
                    .status(inputDTO.getStatus())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_course_progress")
                            .recordId(saved.getProgressId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCourseProgress", saved.getProgressId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserCourseProgress by ID
     */
    public Mono<UserCourseProgressOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCourseProgress", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserCourseProgresss
     */
    public Flux<UserCourseProgressOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserCourseProgresss with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserCourseProgressOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserCourseProgress> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_course_progress", groupIds);
                            Flux<UserCourseProgress> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_course_progress", groupIds, size, offset);
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
     * Update UserCourseProgress
     */
    @Transactional
    public Mono<UserCourseProgressOutputDTO> update(Long id, UserCourseProgressInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCourseProgress", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setLessonId(inputDTO.getLessonId());
                        existing.setCompletionPercentage(inputDTO.getCompletionPercentage());
                        existing.setLastAccessedAt(inputDTO.getLastAccessedAt());
                        existing.setTimeSpentMinutes(inputDTO.getTimeSpentMinutes());
                        existing.setStatus(inputDTO.getStatus());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCourseProgress", saved.getProgressId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserCourseProgress
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCourseProgress", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCourseProgress", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_course_progress", id))
            );
    }
    
    /**
     * Delete UserCourseProgress with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCourseProgress", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCourseProgress", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_course_progress", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserCourseProgressOutputDTO toOutputDTO(UserCourseProgress entity) {
        return UserCourseProgressOutputDTO.builder()
            .progressId(entity.getProgressId())
            .userId(entity.getUserId())
            .courseId(entity.getCourseId())
            .lessonId(entity.getLessonId())
            .completionPercentage(entity.getCompletionPercentage())
            .lastAccessedAt(entity.getLastAccessedAt())
            .timeSpentMinutes(entity.getTimeSpentMinutes())
            .status(entity.getStatus())
            .build();
    }
}