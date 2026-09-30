package com.jobportal.service;

import com.jobportal.entity.TrainingModule;
import com.jobportal.dto.TrainingModuleInputDTO;
import com.jobportal.dto.TrainingModuleOutputDTO;
import com.jobportal.repository.TrainingModuleRepository;
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
 * Service class for TrainingModule business logic.
 */
@Service
@RequiredArgsConstructor
public class TrainingModuleService {
    
    private final TrainingModuleRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new TrainingModule
     */
    @Transactional
    public Mono<TrainingModuleOutputDTO> create(TrainingModuleInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                TrainingModule entity = TrainingModule.builder()
                    .title(inputDTO.getTitle())
                    .description(inputDTO.getDescription())
                    .moduleorder(inputDTO.getModuleorder())
                    .durationminutes(inputDTO.getDurationminutes())
                    .contenturl(inputDTO.getContenturl())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("training_module")
                            .recordId(saved.getTrainingModuleId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingModule", saved.getTrainingModuleId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find TrainingModule by ID
     */
    public Mono<TrainingModuleOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingModule", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all TrainingModules
     */
    public Flux<TrainingModuleOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find TrainingModules with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<TrainingModuleOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<TrainingModule> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "training_module", groupIds);
                            Flux<TrainingModule> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "training_module", groupIds, size, offset);
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
     * Update TrainingModule
     */
    @Transactional
    public Mono<TrainingModuleOutputDTO> update(Long id, TrainingModuleInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingModule", id)))
                    .flatMap(existing -> {
                        existing.setTitle(inputDTO.getTitle());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setModuleorder(inputDTO.getModuleorder());
                        existing.setDurationminutes(inputDTO.getDurationminutes());
                        existing.setContenturl(inputDTO.getContenturl());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingModule", saved.getTrainingModuleId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete TrainingModule
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingModule", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingModule", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("training_module", id))
                    .then()
            );
    }
    
    /**
     * Delete TrainingModule with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingModule", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingModule", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("training_module", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private TrainingModuleOutputDTO toOutputDTO(TrainingModule entity) {
        return TrainingModuleOutputDTO.builder()
            .trainingModuleId(entity.getTrainingModuleId())
            .title(entity.getTitle())
            .description(entity.getDescription())
            .moduleorder(entity.getModuleorder())
            .durationminutes(entity.getDurationminutes())
            .contenturl(entity.getContenturl())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}