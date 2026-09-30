package com.example.service;

import com.example.entity.CourseDocumentGroup;
import com.example.dto.CourseDocumentGroupInputDTO;
import com.example.dto.CourseDocumentGroupOutputDTO;
import com.example.repository.CourseDocumentGroupRepository;
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
 * Service class for CourseDocumentGroup business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseDocumentGroupService {
    
    private final CourseDocumentGroupRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseDocumentGroup
     */
    @Transactional
    public Mono<CourseDocumentGroupOutputDTO> create(CourseDocumentGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseDocumentGroup entity = CourseDocumentGroup.builder()
                    .groupName(inputDTO.getGroupName())
                    .groupDescription(inputDTO.getGroupDescription())
                    .courseId(inputDTO.getCourseId())
                    .isActive(inputDTO.getIsActive())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_document_group")
                            .recordId(saved.getGroupId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseDocumentGroup", saved.getGroupId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseDocumentGroup by ID
     */
    public Mono<CourseDocumentGroupOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseDocumentGroup", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseDocumentGroups
     */
    public Flux<CourseDocumentGroupOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseDocumentGroups with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseDocumentGroupOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseDocumentGroup> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_document_group", groupIds);
                            Flux<CourseDocumentGroup> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_document_group", groupIds, size, offset);
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
     * Update CourseDocumentGroup
     */
    @Transactional
    public Mono<CourseDocumentGroupOutputDTO> update(Long id, CourseDocumentGroupInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseDocumentGroup", id)))
                    .flatMap(existing -> {
                        existing.setGroupName(inputDTO.getGroupName());
                        existing.setGroupDescription(inputDTO.getGroupDescription());
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setIsActive(inputDTO.getIsActive());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseDocumentGroup", saved.getGroupId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseDocumentGroup
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseDocumentGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseDocumentGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_document_group", id))
            );
    }
    
    /**
     * Delete CourseDocumentGroup with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseDocumentGroup", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseDocumentGroup", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_document_group", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CourseDocumentGroupOutputDTO toOutputDTO(CourseDocumentGroup entity) {
        return CourseDocumentGroupOutputDTO.builder()
            .groupId(entity.getGroupId())
            .groupName(entity.getGroupName())
            .groupDescription(entity.getGroupDescription())
            .courseId(entity.getCourseId())
            .isActive(entity.getIsActive())
            .build();
    }
}