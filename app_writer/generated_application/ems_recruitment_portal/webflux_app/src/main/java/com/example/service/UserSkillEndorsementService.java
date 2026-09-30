package com.example.service;

import com.example.entity.UserSkillEndorsement;
import com.example.dto.UserSkillEndorsementInputDTO;
import com.example.dto.UserSkillEndorsementOutputDTO;
import com.example.repository.UserSkillEndorsementRepository;
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
 * Service class for UserSkillEndorsement business logic.
 */
@Service
@RequiredArgsConstructor
public class UserSkillEndorsementService {
    
    private final UserSkillEndorsementRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserSkillEndorsement
     */
    @Transactional
    public Mono<UserSkillEndorsementOutputDTO> create(UserSkillEndorsementInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserSkillEndorsement entity = UserSkillEndorsement.builder()
                    .skillId(inputDTO.getSkillId())
                    .endorsedByUserId(inputDTO.getEndorsedByUserId())
                    .endorsementComment(inputDTO.getEndorsementComment())
                    .relationship(inputDTO.getRelationship())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_skill_endorsement")
                            .recordId(saved.getEndorsementId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserSkillEndorsement", saved.getEndorsementId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserSkillEndorsement by ID
     */
    public Mono<UserSkillEndorsementOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserSkillEndorsement", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserSkillEndorsements
     */
    public Flux<UserSkillEndorsementOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserSkillEndorsements with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserSkillEndorsementOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserSkillEndorsement> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_skill_endorsement", groupIds);
                            Flux<UserSkillEndorsement> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_skill_endorsement", groupIds, size, offset);
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
     * Update UserSkillEndorsement
     */
    @Transactional
    public Mono<UserSkillEndorsementOutputDTO> update(Long id, UserSkillEndorsementInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserSkillEndorsement", id)))
                    .flatMap(existing -> {
                        existing.setSkillId(inputDTO.getSkillId());
                        existing.setEndorsedByUserId(inputDTO.getEndorsedByUserId());
                        existing.setEndorsementComment(inputDTO.getEndorsementComment());
                        existing.setRelationship(inputDTO.getRelationship());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserSkillEndorsement", saved.getEndorsementId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserSkillEndorsement
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserSkillEndorsement", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserSkillEndorsement", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_skill_endorsement", id))
            );
    }
    
    /**
     * Delete UserSkillEndorsement with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserSkillEndorsement", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserSkillEndorsement", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_skill_endorsement", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserSkillEndorsementOutputDTO toOutputDTO(UserSkillEndorsement entity) {
        return UserSkillEndorsementOutputDTO.builder()
            .endorsementId(entity.getEndorsementId())
            .skillId(entity.getSkillId())
            .endorsedByUserId(entity.getEndorsedByUserId())
            .endorsementComment(entity.getEndorsementComment())
            .relationship(entity.getRelationship())
            .build();
    }
}