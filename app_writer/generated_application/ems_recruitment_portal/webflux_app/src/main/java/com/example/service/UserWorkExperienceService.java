package com.example.service;

import com.example.entity.UserWorkExperience;
import com.example.dto.UserWorkExperienceInputDTO;
import com.example.dto.UserWorkExperienceOutputDTO;
import com.example.repository.UserWorkExperienceRepository;
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
 * Service class for UserWorkExperience business logic.
 */
@Service
@RequiredArgsConstructor
public class UserWorkExperienceService {
    
    private final UserWorkExperienceRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserWorkExperience
     */
    @Transactional
    public Mono<UserWorkExperienceOutputDTO> create(UserWorkExperienceInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserWorkExperience entity = UserWorkExperience.builder()
                    .userId(inputDTO.getUserId())
                    .institutionId(inputDTO.getInstitutionId())
                    .jobTitle(inputDTO.getJobTitle())
                    .companyName(inputDTO.getCompanyName())
                    .employmentType(inputDTO.getEmploymentType())
                    .location(inputDTO.getLocation())
                    .startDate(inputDTO.getStartDate())
                    .endDate(inputDTO.getEndDate())
                    .isCurrent(inputDTO.getIsCurrent())
                    .responsibilities(inputDTO.getResponsibilities())
                    .achievements(inputDTO.getAchievements())
                    .skillsUsed(inputDTO.getSkillsUsed())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_work_experience")
                            .recordId(saved.getExperienceId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserWorkExperience", saved.getExperienceId(),
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
                        existing.setUserId(inputDTO.getUserId());
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setJobTitle(inputDTO.getJobTitle());
                        existing.setCompanyName(inputDTO.getCompanyName());
                        existing.setEmploymentType(inputDTO.getEmploymentType());
                        existing.setLocation(inputDTO.getLocation());
                        existing.setStartDate(inputDTO.getStartDate());
                        existing.setEndDate(inputDTO.getEndDate());
                        existing.setIsCurrent(inputDTO.getIsCurrent());
                        existing.setResponsibilities(inputDTO.getResponsibilities());
                        existing.setAchievements(inputDTO.getAchievements());
                        existing.setSkillsUsed(inputDTO.getSkillsUsed());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserWorkExperience", saved.getExperienceId(),
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
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserWorkExperienceOutputDTO toOutputDTO(UserWorkExperience entity) {
        return UserWorkExperienceOutputDTO.builder()
            .experienceId(entity.getExperienceId())
            .userId(entity.getUserId())
            .institutionId(entity.getInstitutionId())
            .jobTitle(entity.getJobTitle())
            .companyName(entity.getCompanyName())
            .employmentType(entity.getEmploymentType())
            .location(entity.getLocation())
            .startDate(entity.getStartDate())
            .endDate(entity.getEndDate())
            .isCurrent(entity.getIsCurrent())
            .responsibilities(entity.getResponsibilities())
            .achievements(entity.getAchievements())
            .skillsUsed(entity.getSkillsUsed())
            .build();
    }
}