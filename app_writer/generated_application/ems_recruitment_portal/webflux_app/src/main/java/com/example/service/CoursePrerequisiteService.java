package com.example.service;

import com.example.entity.CoursePrerequisite;
import com.example.dto.CoursePrerequisiteInputDTO;
import com.example.dto.CoursePrerequisiteOutputDTO;
import com.example.repository.CoursePrerequisiteRepository;
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
 * Service class for CoursePrerequisite business logic.
 */
@Service
@RequiredArgsConstructor
public class CoursePrerequisiteService {
    
    private final CoursePrerequisiteRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CoursePrerequisite
     */
    @Transactional
    public Mono<CoursePrerequisiteOutputDTO> create(CoursePrerequisiteInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CoursePrerequisite entity = CoursePrerequisite.builder()
                    .courseId(inputDTO.getCourseId())
                    .prerequisiteCourseId(inputDTO.getPrerequisiteCourseId())
                    .prerequisiteType(inputDTO.getPrerequisiteType())
                    .prerequisiteDescription(inputDTO.getPrerequisiteDescription())
                    .isMandatory(inputDTO.getIsMandatory())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_prerequisite")
                            .recordId(saved.getPrerequisiteId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CoursePrerequisite", saved.getPrerequisiteId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CoursePrerequisite by ID
     */
    public Mono<CoursePrerequisiteOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CoursePrerequisite", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CoursePrerequisites
     */
    public Flux<CoursePrerequisiteOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CoursePrerequisites with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CoursePrerequisiteOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CoursePrerequisite> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_prerequisite", groupIds);
                            Flux<CoursePrerequisite> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_prerequisite", groupIds, size, offset);
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
     * Update CoursePrerequisite
     */
    @Transactional
    public Mono<CoursePrerequisiteOutputDTO> update(Long id, CoursePrerequisiteInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CoursePrerequisite", id)))
                    .flatMap(existing -> {
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setPrerequisiteCourseId(inputDTO.getPrerequisiteCourseId());
                        existing.setPrerequisiteType(inputDTO.getPrerequisiteType());
                        existing.setPrerequisiteDescription(inputDTO.getPrerequisiteDescription());
                        existing.setIsMandatory(inputDTO.getIsMandatory());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CoursePrerequisite", saved.getPrerequisiteId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CoursePrerequisite
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CoursePrerequisite", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CoursePrerequisite", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_prerequisite", id))
            );
    }
    
    /**
     * Delete CoursePrerequisite with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CoursePrerequisite", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CoursePrerequisite", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_prerequisite", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CoursePrerequisiteOutputDTO toOutputDTO(CoursePrerequisite entity) {
        return CoursePrerequisiteOutputDTO.builder()
            .prerequisiteId(entity.getPrerequisiteId())
            .courseId(entity.getCourseId())
            .prerequisiteCourseId(entity.getPrerequisiteCourseId())
            .prerequisiteType(entity.getPrerequisiteType())
            .prerequisiteDescription(entity.getPrerequisiteDescription())
            .isMandatory(entity.getIsMandatory())
            .build();
    }
}