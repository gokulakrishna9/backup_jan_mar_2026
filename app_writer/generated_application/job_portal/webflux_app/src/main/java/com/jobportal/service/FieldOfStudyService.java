package com.jobportal.service;

import com.jobportal.entity.FieldOfStudy;
import com.jobportal.dto.FieldOfStudyInputDTO;
import com.jobportal.dto.FieldOfStudyOutputDTO;
import com.jobportal.repository.FieldOfStudyRepository;
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
 * Service class for FieldOfStudy business logic.
 */
@Service
@RequiredArgsConstructor
public class FieldOfStudyService {
    
    private final FieldOfStudyRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new FieldOfStudy
     */
    @Transactional
    public Mono<FieldOfStudyOutputDTO> create(FieldOfStudyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                FieldOfStudy entity = FieldOfStudy.builder()
                    .name(inputDTO.getName())
                    .description(inputDTO.getDescription())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("field_of_study")
                            .recordId(saved.getFieldOfStudyId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "FieldOfStudy", saved.getFieldOfStudyId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find FieldOfStudy by ID
     */
    public Mono<FieldOfStudyOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("FieldOfStudy", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all FieldOfStudys
     */
    public Flux<FieldOfStudyOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find FieldOfStudys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<FieldOfStudyOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<FieldOfStudy> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "field_of_study", groupIds);
                            Flux<FieldOfStudy> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "field_of_study", groupIds, size, offset);
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
     * Update FieldOfStudy
     */
    @Transactional
    public Mono<FieldOfStudyOutputDTO> update(Long id, FieldOfStudyInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("FieldOfStudy", id)))
                    .flatMap(existing -> {
                        existing.setName(inputDTO.getName());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "FieldOfStudy", saved.getFieldOfStudyId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete FieldOfStudy
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("FieldOfStudy", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "FieldOfStudy", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("field_of_study", id))
                    .then()
            );
    }
    
    /**
     * Delete FieldOfStudy with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("FieldOfStudy", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "FieldOfStudy", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("field_of_study", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private FieldOfStudyOutputDTO toOutputDTO(FieldOfStudy entity) {
        return FieldOfStudyOutputDTO.builder()
            .fieldOfStudyId(entity.getFieldOfStudyId())
            .name(entity.getName())
            .description(entity.getDescription())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}