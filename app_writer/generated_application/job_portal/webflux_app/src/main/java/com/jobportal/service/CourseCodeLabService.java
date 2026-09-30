package com.jobportal.service;

import com.jobportal.entity.CourseCodeLab;
import com.jobportal.dto.CourseCodeLabInputDTO;
import com.jobportal.dto.CourseCodeLabOutputDTO;
import com.jobportal.repository.CourseCodeLabRepository;
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
 * Service class for CourseCodeLab business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseCodeLabService {
    
    private final CourseCodeLabRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseCodeLab
     */
    @Transactional
    public Mono<CourseCodeLabOutputDTO> create(CourseCodeLabInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseCodeLab entity = CourseCodeLab.builder()
                    .title(inputDTO.getTitle())
                    .description(inputDTO.getDescription())
                    .language(inputDTO.getLanguage())
                    .startercode(inputDTO.getStartercode())
                    .solutioncode(inputDTO.getSolutioncode())
                    .instructions(inputDTO.getInstructions())
                    .sortorder(inputDTO.getSortorder())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_code_lab")
                            .recordId(saved.getCourseCodeLabId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseCodeLab", saved.getCourseCodeLabId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseCodeLab by ID
     */
    public Mono<CourseCodeLabOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseCodeLab", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseCodeLabs
     */
    public Flux<CourseCodeLabOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseCodeLabs with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseCodeLabOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseCodeLab> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_code_lab", groupIds);
                            Flux<CourseCodeLab> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_code_lab", groupIds, size, offset);
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
     * Update CourseCodeLab
     */
    @Transactional
    public Mono<CourseCodeLabOutputDTO> update(Long id, CourseCodeLabInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseCodeLab", id)))
                    .flatMap(existing -> {
                        existing.setTitle(inputDTO.getTitle());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setLanguage(inputDTO.getLanguage());
                        existing.setStartercode(inputDTO.getStartercode());
                        existing.setSolutioncode(inputDTO.getSolutioncode());
                        existing.setInstructions(inputDTO.getInstructions());
                        existing.setSortorder(inputDTO.getSortorder());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseCodeLab", saved.getCourseCodeLabId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseCodeLab
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseCodeLab", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseCodeLab", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_code_lab", id))
                    .then()
            );
    }
    
    /**
     * Delete CourseCodeLab with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseCodeLab", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseCodeLab", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_code_lab", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private CourseCodeLabOutputDTO toOutputDTO(CourseCodeLab entity) {
        return CourseCodeLabOutputDTO.builder()
            .courseCodeLabId(entity.getCourseCodeLabId())
            .title(entity.getTitle())
            .description(entity.getDescription())
            .language(entity.getLanguage())
            .startercode(entity.getStartercode())
            .solutioncode(entity.getSolutioncode())
            .instructions(entity.getInstructions())
            .sortorder(entity.getSortorder())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}