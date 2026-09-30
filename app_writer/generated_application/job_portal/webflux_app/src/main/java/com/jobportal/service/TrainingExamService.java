package com.jobportal.service;

import com.jobportal.entity.TrainingExam;
import com.jobportal.dto.TrainingExamInputDTO;
import com.jobportal.dto.TrainingExamOutputDTO;
import com.jobportal.repository.TrainingExamRepository;
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
 * Service class for TrainingExam business logic.
 */
@Service
@RequiredArgsConstructor
public class TrainingExamService {
    
    private final TrainingExamRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new TrainingExam
     */
    @Transactional
    public Mono<TrainingExamOutputDTO> create(TrainingExamInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                TrainingExam entity = TrainingExam.builder()
                    .title(inputDTO.getTitle())
                    .description(inputDTO.getDescription())
                    .passingscore(inputDTO.getPassingscore())
                    .maxscore(inputDTO.getMaxscore())
                    .timelimitminutes(inputDTO.getTimelimitminutes())
                    .maxattempts(inputDTO.getMaxattempts())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("training_exam")
                            .recordId(saved.getTrainingExamId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingExam", saved.getTrainingExamId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find TrainingExam by ID
     */
    public Mono<TrainingExamOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingExam", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all TrainingExams
     */
    public Flux<TrainingExamOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find TrainingExams with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<TrainingExamOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<TrainingExam> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "training_exam", groupIds);
                            Flux<TrainingExam> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "training_exam", groupIds, size, offset);
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
     * Update TrainingExam
     */
    @Transactional
    public Mono<TrainingExamOutputDTO> update(Long id, TrainingExamInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingExam", id)))
                    .flatMap(existing -> {
                        existing.setTitle(inputDTO.getTitle());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setPassingscore(inputDTO.getPassingscore());
                        existing.setMaxscore(inputDTO.getMaxscore());
                        existing.setTimelimitminutes(inputDTO.getTimelimitminutes());
                        existing.setMaxattempts(inputDTO.getMaxattempts());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingExam", saved.getTrainingExamId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete TrainingExam
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingExam", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingExam", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("training_exam", id))
                    .then()
            );
    }
    
    /**
     * Delete TrainingExam with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("TrainingExam", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "TrainingExam", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("training_exam", id))
                    .then()
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private TrainingExamOutputDTO toOutputDTO(TrainingExam entity) {
        return TrainingExamOutputDTO.builder()
            .trainingExamId(entity.getTrainingExamId())
            .title(entity.getTitle())
            .description(entity.getDescription())
            .passingscore(entity.getPassingscore())
            .maxscore(entity.getMaxscore())
            .timelimitminutes(entity.getTimelimitminutes())
            .maxattempts(entity.getMaxattempts())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}