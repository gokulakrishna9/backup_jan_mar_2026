package com.jobportal.service;

import com.jobportal.entity.StudentProfile;
import com.jobportal.dto.StudentProfileInputDTO;
import com.jobportal.dto.StudentProfileOutputDTO;
import com.jobportal.repository.StudentProfileRepository;
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
 * Service class for StudentProfile business logic.
 */
@Service
@RequiredArgsConstructor
public class StudentProfileService {
    
    private final StudentProfileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new StudentProfile
     */
    @Transactional
    public Mono<StudentProfileOutputDTO> create(StudentProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                // Single-record-per-user: reject if user already owns a record
                return repository.findByOwnerUserId(user.getAuthUserId())
                    .flatMap(existing -> Mono.<StudentProfile>error(
                        new IllegalStateException("StudentProfile: only one record per user is allowed")))
                    .switchIfEmpty(Mono.defer(() -> {
                        StudentProfile entity = StudentProfile.builder()
                            .resumeurl(inputDTO.getResumeurl())
                            .skills(inputDTO.getSkills())
                            .educationlevel(inputDTO.getEducationlevel())
                            .createdAt(LocalDateTime.now())
                            .updatedAt(LocalDateTime.now())
                            .build();
                        
                        return repository.save(entity)
                            .flatMap(saved -> {
                                RecordOwner recordOwner = RecordOwner.builder()
                                    .authUserId(user.getAuthUserId())
                                    .tableName("student_profile")
                                    .recordId(saved.getStudentProfileId())
                                    .createdAt(LocalDateTime.now())
                                    .build();
                                return recordOwnerRepository.save(recordOwner)
                                    .thenReturn(saved);
                            });
                    }))
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "StudentProfile", saved.getStudentProfileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find StudentProfile by ID
     */
    public Mono<StudentProfileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("StudentProfile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all StudentProfiles
     */
    public Flux<StudentProfileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find StudentProfiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<StudentProfileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<StudentProfile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "student_profile", groupIds);
                            Flux<StudentProfile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "student_profile", groupIds, size, offset);
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
     * Update StudentProfile
     */
    @Transactional
    public Mono<StudentProfileOutputDTO> update(Long id, StudentProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("StudentProfile", id)))
                    .flatMap(existing -> {
                        existing.setResumeurl(inputDTO.getResumeurl());
                        existing.setSkills(inputDTO.getSkills());
                        existing.setEducationlevel(inputDTO.getEducationlevel());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "StudentProfile", saved.getStudentProfileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete StudentProfile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("StudentProfile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "StudentProfile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("student_profile", id))
                    .then()
            );
    }
    
    /**
     * Delete StudentProfile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("StudentProfile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "StudentProfile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("student_profile", id))
                    .then()
            );
    }
    
    /**
     * Find the current user's own StudentProfile record (single-record-per-user).
     */
    public Mono<StudentProfileOutputDTO> findMyRecord() {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> repository.findByOwnerUserId(user.getAuthUserId()))
            .map(this::toOutputDTO);
    }

    /**
     * Convert entity to output DTO
     */
    private StudentProfileOutputDTO toOutputDTO(StudentProfile entity) {
        return StudentProfileOutputDTO.builder()
            .studentProfileId(entity.getStudentProfileId())
            .resumeurl(entity.getResumeurl())
            .skills(entity.getSkills())
            .educationlevel(entity.getEducationlevel())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}