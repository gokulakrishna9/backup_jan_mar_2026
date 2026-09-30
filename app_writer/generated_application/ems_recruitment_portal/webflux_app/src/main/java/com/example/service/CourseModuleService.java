package com.example.service;

import com.example.entity.CourseModule;
import com.example.dto.CourseModuleInputDTO;
import com.example.dto.CourseModuleOutputDTO;
import com.example.repository.CourseModuleRepository;
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
 * Service class for CourseModule business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseModuleService {
    
    private final CourseModuleRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseModule
     */
    @Transactional
    public Mono<CourseModuleOutputDTO> create(CourseModuleInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseModule entity = CourseModule.builder()
                    .courseId(inputDTO.getCourseId())
                    .moduleName(inputDTO.getModuleName())
                    .moduleNumber(inputDTO.getModuleNumber())
                    .description(inputDTO.getDescription())
                    .durationHours(inputDTO.getDurationHours())
                    .learningObjectives(inputDTO.getLearningObjectives())
                    .isMandatory(inputDTO.getIsMandatory())
                    .orderSequence(inputDTO.getOrderSequence())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_module")
                            .recordId(saved.getModuleId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseModule", saved.getModuleId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseModule by ID
     */
    public Mono<CourseModuleOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseModule", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseModules
     */
    public Flux<CourseModuleOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseModules with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseModuleOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseModule> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_module", groupIds);
                            Flux<CourseModule> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_module", groupIds, size, offset);
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
     * Update CourseModule
     */
    @Transactional
    public Mono<CourseModuleOutputDTO> update(Long id, CourseModuleInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseModule", id)))
                    .flatMap(existing -> {
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setModuleName(inputDTO.getModuleName());
                        existing.setModuleNumber(inputDTO.getModuleNumber());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setDurationHours(inputDTO.getDurationHours());
                        existing.setLearningObjectives(inputDTO.getLearningObjectives());
                        existing.setIsMandatory(inputDTO.getIsMandatory());
                        existing.setOrderSequence(inputDTO.getOrderSequence());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseModule", saved.getModuleId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseModule
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseModule", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseModule", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_module", id))
            );
    }
    
    /**
     * Delete CourseModule with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseModule", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseModule", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_module", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CourseModuleOutputDTO toOutputDTO(CourseModule entity) {
        return CourseModuleOutputDTO.builder()
            .moduleId(entity.getModuleId())
            .courseId(entity.getCourseId())
            .moduleName(entity.getModuleName())
            .moduleNumber(entity.getModuleNumber())
            .description(entity.getDescription())
            .durationHours(entity.getDurationHours())
            .learningObjectives(entity.getLearningObjectives())
            .isMandatory(entity.getIsMandatory())
            .orderSequence(entity.getOrderSequence())
            .build();
    }
}