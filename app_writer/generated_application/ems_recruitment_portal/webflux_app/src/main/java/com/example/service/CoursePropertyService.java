package com.example.service;

import com.example.entity.CourseProperty;
import com.example.dto.CoursePropertyInputDTO;
import com.example.dto.CoursePropertyOutputDTO;
import com.example.repository.CoursePropertyRepository;
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
 * Service class for CourseProperty business logic.
 */
@Service
@RequiredArgsConstructor
public class CoursePropertyService {
    
    private final CoursePropertyRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseProperty
     */
    @Transactional
    public Mono<CoursePropertyOutputDTO> create(CoursePropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseProperty entity = CourseProperty.builder()
                    .propertyName(inputDTO.getPropertyName())
                    .propertyValue(inputDTO.getPropertyValue())
                    .propertyType(inputDTO.getPropertyType())
                    .propertyDescription(inputDTO.getPropertyDescription())
                    .groupId(inputDTO.getGroupId())
                    .courseId(inputDTO.getCourseId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_property")
                            .recordId(saved.getPropertyId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseProperty", saved.getPropertyId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseProperty by ID
     */
    public Mono<CoursePropertyOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseProperty", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CoursePropertys
     */
    public Flux<CoursePropertyOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CoursePropertys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CoursePropertyOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseProperty> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_property", groupIds);
                            Flux<CourseProperty> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_property", groupIds, size, offset);
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
     * Update CourseProperty
     */
    @Transactional
    public Mono<CoursePropertyOutputDTO> update(Long id, CoursePropertyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseProperty", id)))
                    .flatMap(existing -> {
                        existing.setPropertyName(inputDTO.getPropertyName());
                        existing.setPropertyValue(inputDTO.getPropertyValue());
                        existing.setPropertyType(inputDTO.getPropertyType());
                        existing.setPropertyDescription(inputDTO.getPropertyDescription());
                        existing.setGroupId(inputDTO.getGroupId());
                        existing.setCourseId(inputDTO.getCourseId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseProperty", saved.getPropertyId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseProperty
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_property", id))
            );
    }
    
    /**
     * Delete CourseProperty with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseProperty", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseProperty", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_property", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CoursePropertyOutputDTO toOutputDTO(CourseProperty entity) {
        return CoursePropertyOutputDTO.builder()
            .propertyId(entity.getPropertyId())
            .propertyName(entity.getPropertyName())
            .propertyValue(entity.getPropertyValue())
            .propertyType(entity.getPropertyType())
            .propertyDescription(entity.getPropertyDescription())
            .groupId(entity.getGroupId())
            .courseId(entity.getCourseId())
            .build();
    }
}