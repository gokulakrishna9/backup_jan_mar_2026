package com.example.service;

import com.example.entity.Course;
import com.example.dto.CourseInputDTO;
import com.example.dto.CourseOutputDTO;
import com.example.repository.CourseRepository;
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
 * Service class for Course business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseService {
    
    private final CourseRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new Course
     */
    @Transactional
    public Mono<CourseOutputDTO> create(CourseInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                Course entity = Course.builder()
                    .courseName(inputDTO.getCourseName())
                    .description(inputDTO.getDescription())
                    .outcomes(inputDTO.getOutcomes())
                    .courseTypeId(inputDTO.getCourseTypeId())
                    .isPublished(inputDTO.getIsPublished())
                    .price(inputDTO.getPrice())
                    .durationWeeks(inputDTO.getDurationWeeks())
                    .institutionId(inputDTO.getInstitutionId())
                    .isEntity(inputDTO.getIsEntity())
                    .isPublic(inputDTO.getIsPublic())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course")
                            .recordId(saved.getCourseId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "Course", saved.getCourseId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find Course by ID
     */
    public Mono<CourseOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("Course", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all Courses
     */
    public Flux<CourseOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find Courses with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<Course> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course", groupIds);
                            Flux<Course> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course", groupIds, size, offset);
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
     * Update Course
     */
    @Transactional
    public Mono<CourseOutputDTO> update(Long id, CourseInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Course", id)))
                    .flatMap(existing -> {
                        existing.setCourseName(inputDTO.getCourseName());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setOutcomes(inputDTO.getOutcomes());
                        existing.setCourseTypeId(inputDTO.getCourseTypeId());
                        existing.setIsPublished(inputDTO.getIsPublished());
                        existing.setPrice(inputDTO.getPrice());
                        existing.setDurationWeeks(inputDTO.getDurationWeeks());
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setIsEntity(inputDTO.getIsEntity());
                        existing.setIsPublic(inputDTO.getIsPublic());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "Course", saved.getCourseId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete Course
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Course", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Course", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course", id))
            );
    }
    
    /**
     * Delete Course with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Course", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Course", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CourseOutputDTO toOutputDTO(Course entity) {
        return CourseOutputDTO.builder()
            .courseId(entity.getCourseId())
            .courseName(entity.getCourseName())
            .description(entity.getDescription())
            .outcomes(entity.getOutcomes())
            .courseTypeId(entity.getCourseTypeId())
            .isPublished(entity.getIsPublished())
            .price(entity.getPrice())
            .durationWeeks(entity.getDurationWeeks())
            .institutionId(entity.getInstitutionId())
            .isEntity(entity.getIsEntity())
            .isPublic(entity.getIsPublic())
            .build();
    }
}