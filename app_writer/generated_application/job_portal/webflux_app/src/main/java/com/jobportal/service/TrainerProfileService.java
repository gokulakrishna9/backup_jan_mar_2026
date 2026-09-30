package com.jobportal.service;

import com.jobportal.entity.TrainerProfile;
import com.jobportal.dto.TrainerProfileInputDTO;
import com.jobportal.dto.TrainerProfileOutputDTO;
import com.jobportal.repository.TrainerProfileRepository;
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
 * Service class for TrainerProfile business logic.
 */
@Service
@RequiredArgsConstructor
public class TrainerProfileService {
    
    private final TrainerProfileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new TrainerProfile
     */
    @Transactional
    public Mono<TrainerProfileOutputDTO> create(TrainerProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                // Single-record-per-user: reject if user already owns a record
                return repository.findByOwnerUserId(user.getAuthUserId())
                    .flatMap(existing -> Mono.<TrainerProfile>error(
                        new IllegalStateException("TrainerProfile: only one record per user is allowed")))
                    .switchIfEmpty(Mono.defer(() -> {
                        TrainerProfile entity = TrainerProfile.builder()
                            .specialization(inputDTO.getSpecialization())
                            .certifications(inputDTO.getCertifications())
                            .hourlyrate(inputDTO.getHourlyrate())
                            .createdAt(LocalDateTime.now())
                            .updatedAt(LocalDateTime.now())
                            .build();
                        
                        return repository.save(entity)
                            .flatMap(saved -> {
                                RecordOwner recordOwner = RecordOwner.builder()
                                    .authUserId(user.getAuthUserId())
                                    .tableName("trainer_profile")
                                    .recordId(saved.getTrainerProfileId())
                                    .createdAt(LocalDateTime.now())
                                    .build();
                                return recordOwnerRepository.save(recordOwner)
                                    .thenReturn(saved);
                            });
                    }))
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainerProfile", saved.getTrainerProfileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find TrainerProfile by ID
     */
    public Mono<TrainerProfileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainerProfile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all TrainerProfiles
     */
    public Flux<TrainerProfileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find TrainerProfiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<TrainerProfileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<TrainerProfile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "trainer_profile", groupIds);
                            Flux<TrainerProfile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "trainer_profile", groupIds, size, offset);
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
     * Update TrainerProfile
     */
    @Transactional
    public Mono<TrainerProfileOutputDTO> update(Long id, TrainerProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainerProfile", id)))
                    .flatMap(existing -> {
                        existing.setSpecialization(inputDTO.getSpecialization());
                        existing.setCertifications(inputDTO.getCertifications());
                        existing.setHourlyrate(inputDTO.getHourlyrate());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainerProfile", saved.getTrainerProfileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete TrainerProfile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainerProfile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainerProfile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("trainer_profile", id))
                    .then()
            );
    }
    
    /**
     * Delete TrainerProfile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainerProfile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainerProfile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("trainer_profile", id))
                    .then()
            );
    }
    
    /**
     * Find the current user's own TrainerProfile record (single-record-per-user).
     */
    public Mono<TrainerProfileOutputDTO> findMyRecord() {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> repository.findByOwnerUserId(user.getAuthUserId()))
            .map(this::toOutputDTO);
    }

    /**
     * Convert entity to output DTO
     */
    private TrainerProfileOutputDTO toOutputDTO(TrainerProfile entity) {
        return TrainerProfileOutputDTO.builder()
            .trainerProfileId(entity.getTrainerProfileId())
            .specialization(entity.getSpecialization())
            .certifications(entity.getCertifications())
            .hourlyrate(entity.getHourlyrate())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}