package com.jobportal.service;

import com.jobportal.entity.UserWorkExperience;
import com.jobportal.dto.UserWorkExperienceInputDTO;
import com.jobportal.dto.UserWorkExperienceOutputDTO;
import com.jobportal.repository.UserWorkExperienceRepository;
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
 * Service class for UserWorkExperience business logic.
 */
@Service
@RequiredArgsConstructor
public class UserWorkExperienceService {
    
    private final UserWorkExperienceRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserWorkExperience
     */
    @Transactional
    public Mono<UserWorkExperienceOutputDTO> create(UserWorkExperienceInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserWorkExperience entity = UserWorkExperience.builder()
                    .companyname(inputDTO.getCompanyname())
                    .jobtitle(inputDTO.getJobtitle())
                    .industry(inputDTO.getIndustry())
                    .location(inputDTO.getLocation())
                    .startdate(inputDTO.getStartdate())
                    .enddate(inputDTO.getEnddate())
                    .iscurrent(inputDTO.getIscurrent())
                    .description(inputDTO.getDescription())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_work_experience")
                            .recordId(saved.getUserWorkExperienceId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserWorkExperience", saved.getUserWorkExperienceId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserWorkExperience by ID
     */
    public Mono<UserWorkExperienceOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserWorkExperience", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserWorkExperiences
     */
    public Flux<UserWorkExperienceOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserWorkExperiences with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserWorkExperienceOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserWorkExperience> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_work_experience", groupIds);
                            Flux<UserWorkExperience> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_work_experience", groupIds, size, offset);
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
     * Update UserWorkExperience
     */
    @Transactional
    public Mono<UserWorkExperienceOutputDTO> update(Long id, UserWorkExperienceInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserWorkExperience", id)))
                    .flatMap(existing -> {
                        existing.setCompanyname(inputDTO.getCompanyname());
                        existing.setJobtitle(inputDTO.getJobtitle());
                        existing.setIndustry(inputDTO.getIndustry());
                        existing.setLocation(inputDTO.getLocation());
                        existing.setStartdate(inputDTO.getStartdate());
                        existing.setEnddate(inputDTO.getEnddate());
                        existing.setIscurrent(inputDTO.getIscurrent());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserWorkExperience", saved.getUserWorkExperienceId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserWorkExperience
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserWorkExperience", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserWorkExperience", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_work_experience", id))
                    .then()
            );
    }
    
    /**
     * Delete UserWorkExperience with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserWorkExperience", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserWorkExperience", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_work_experience", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private UserWorkExperienceOutputDTO toOutputDTO(UserWorkExperience entity) {
        return UserWorkExperienceOutputDTO.builder()
            .userWorkExperienceId(entity.getUserWorkExperienceId())
            .companyname(entity.getCompanyname())
            .jobtitle(entity.getJobtitle())
            .industry(entity.getIndustry())
            .location(entity.getLocation())
            .startdate(entity.getStartdate())
            .enddate(entity.getEnddate())
            .iscurrent(entity.getIscurrent())
            .description(entity.getDescription())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}