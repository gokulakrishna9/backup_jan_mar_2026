package com.example.service;

import com.example.entity.CourseLesson;
import com.example.dto.CourseLessonInputDTO;
import com.example.dto.CourseLessonOutputDTO;
import com.example.repository.CourseLessonRepository;
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
 * Service class for CourseLesson business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseLessonService {
    
    private final CourseLessonRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseLesson
     */
    @Transactional
    public Mono<CourseLessonOutputDTO> create(CourseLessonInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseLesson entity = CourseLesson.builder()
                    .moduleId(inputDTO.getModuleId())
                    .courseId(inputDTO.getCourseId())
                    .lessonTitle(inputDTO.getLessonTitle())
                    .lessonNumber(inputDTO.getLessonNumber())
                    .contentType(inputDTO.getContentType())
                    .contentUrl(inputDTO.getContentUrl())
                    .durationMinutes(inputDTO.getDurationMinutes())
                    .isPreviewAvailable(inputDTO.getIsPreviewAvailable())
                    .orderSequence(inputDTO.getOrderSequence())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_lesson")
                            .recordId(saved.getLessonId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseLesson", saved.getLessonId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseLesson by ID
     */
    public Mono<CourseLessonOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseLesson", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseLessons
     */
    public Flux<CourseLessonOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseLessons with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseLessonOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseLesson> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_lesson", groupIds);
                            Flux<CourseLesson> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_lesson", groupIds, size, offset);
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
     * Update CourseLesson
     */
    @Transactional
    public Mono<CourseLessonOutputDTO> update(Long id, CourseLessonInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseLesson", id)))
                    .flatMap(existing -> {
                        existing.setModuleId(inputDTO.getModuleId());
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setLessonTitle(inputDTO.getLessonTitle());
                        existing.setLessonNumber(inputDTO.getLessonNumber());
                        existing.setContentType(inputDTO.getContentType());
                        existing.setContentUrl(inputDTO.getContentUrl());
                        existing.setDurationMinutes(inputDTO.getDurationMinutes());
                        existing.setIsPreviewAvailable(inputDTO.getIsPreviewAvailable());
                        existing.setOrderSequence(inputDTO.getOrderSequence());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseLesson", saved.getLessonId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseLesson
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseLesson", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseLesson", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_lesson", id))
            );
    }
    
    /**
     * Delete CourseLesson with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseLesson", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseLesson", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_lesson", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CourseLessonOutputDTO toOutputDTO(CourseLesson entity) {
        return CourseLessonOutputDTO.builder()
            .lessonId(entity.getLessonId())
            .moduleId(entity.getModuleId())
            .courseId(entity.getCourseId())
            .lessonTitle(entity.getLessonTitle())
            .lessonNumber(entity.getLessonNumber())
            .contentType(entity.getContentType())
            .contentUrl(entity.getContentUrl())
            .durationMinutes(entity.getDurationMinutes())
            .isPreviewAvailable(entity.getIsPreviewAvailable())
            .orderSequence(entity.getOrderSequence())
            .build();
    }
}