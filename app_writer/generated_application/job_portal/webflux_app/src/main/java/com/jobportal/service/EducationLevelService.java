package com.jobportal.service;

import com.jobportal.entity.EducationLevel;
import com.jobportal.dto.EducationLevelInputDTO;
import com.jobportal.dto.EducationLevelOutputDTO;
import com.jobportal.repository.EducationLevelRepository;
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
 * Service class for EducationLevel business logic.
 */
@Service
@RequiredArgsConstructor
public class EducationLevelService {
    
    private final EducationLevelRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new EducationLevel
     */
    @Transactional
    public Mono<EducationLevelOutputDTO> create(EducationLevelInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                EducationLevel entity = EducationLevel.builder()
                    .name(inputDTO.getName())
                    .description(inputDTO.getDescription())
                    .sortorder(inputDTO.getSortorder())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("education_level")
                            .recordId(saved.getEducationLevelId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "EducationLevel", saved.getEducationLevelId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find EducationLevel by ID
     */
    public Mono<EducationLevelOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("EducationLevel", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all EducationLevels
     */
    public Flux<EducationLevelOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find EducationLevels with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<EducationLevelOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<EducationLevel> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "education_level", groupIds);
                            Flux<EducationLevel> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "education_level", groupIds, size, offset);
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
     * Update EducationLevel
     */
    @Transactional
    public Mono<EducationLevelOutputDTO> update(Long id, EducationLevelInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("EducationLevel", id)))
                    .flatMap(existing -> {
                        existing.setName(inputDTO.getName());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setSortorder(inputDTO.getSortorder());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "EducationLevel", saved.getEducationLevelId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete EducationLevel
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("EducationLevel", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "EducationLevel", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("education_level", id))
                    .then()
            );
    }
    
    /**
     * Delete EducationLevel with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("EducationLevel", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "EducationLevel", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("education_level", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private EducationLevelOutputDTO toOutputDTO(EducationLevel entity) {
        return EducationLevelOutputDTO.builder()
            .educationLevelId(entity.getEducationLevelId())
            .name(entity.getName())
            .description(entity.getDescription())
            .sortorder(entity.getSortorder())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}