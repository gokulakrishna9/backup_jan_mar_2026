package com.example.service;

import com.example.entity.CourseInstructor;
import com.example.dto.CourseInstructorInputDTO;
import com.example.dto.CourseInstructorOutputDTO;
import com.example.repository.CourseInstructorRepository;
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
 * Service class for CourseInstructor business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseInstructorService {
    
    private final CourseInstructorRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseInstructor
     */
    @Transactional
    public Mono<CourseInstructorOutputDTO> create(CourseInstructorInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseInstructor entity = CourseInstructor.builder()
                    .courseId(inputDTO.getCourseId())
                    .userId(inputDTO.getUserId())
                    .role(inputDTO.getRole())
                    .bio(inputDTO.getBio())
                    .specialization(inputDTO.getSpecialization())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_instructor")
                            .recordId(saved.getInstructorLinkId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseInstructor", saved.getInstructorLinkId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseInstructor by ID
     */
    public Mono<CourseInstructorOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseInstructor", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseInstructors
     */
    public Flux<CourseInstructorOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseInstructors with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseInstructorOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseInstructor> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_instructor", groupIds);
                            Flux<CourseInstructor> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_instructor", groupIds, size, offset);
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
     * Update CourseInstructor
     */
    @Transactional
    public Mono<CourseInstructorOutputDTO> update(Long id, CourseInstructorInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseInstructor", id)))
                    .flatMap(existing -> {
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setUserId(inputDTO.getUserId());
                        existing.setRole(inputDTO.getRole());
                        existing.setBio(inputDTO.getBio());
                        existing.setSpecialization(inputDTO.getSpecialization());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseInstructor", saved.getInstructorLinkId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseInstructor
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseInstructor", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseInstructor", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_instructor", id))
            );
    }
    
    /**
     * Delete CourseInstructor with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseInstructor", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseInstructor", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_instructor", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CourseInstructorOutputDTO toOutputDTO(CourseInstructor entity) {
        return CourseInstructorOutputDTO.builder()
            .instructorLinkId(entity.getInstructorLinkId())
            .courseId(entity.getCourseId())
            .userId(entity.getUserId())
            .role(entity.getRole())
            .bio(entity.getBio())
            .specialization(entity.getSpecialization())
            .build();
    }
}