package com.example.service;

import com.example.entity.UserAchievement;
import com.example.dto.UserAchievementInputDTO;
import com.example.dto.UserAchievementOutputDTO;
import com.example.repository.UserAchievementRepository;
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
 * Service class for UserAchievement business logic.
 */
@Service
@RequiredArgsConstructor
public class UserAchievementService {
    
    private final UserAchievementRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserAchievement
     */
    @Transactional
    public Mono<UserAchievementOutputDTO> create(UserAchievementInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserAchievement entity = UserAchievement.builder()
                    .userId(inputDTO.getUserId())
                    .title(inputDTO.getTitle())
                    .description(inputDTO.getDescription())
                    .achievementType(inputDTO.getAchievementType())
                    .issuer(inputDTO.getIssuer())
                    .dateAchieved(inputDTO.getDateAchieved())
                    .url(inputDTO.getUrl())
                    .documentId(inputDTO.getDocumentId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_achievement")
                            .recordId(saved.getAchievementId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserAchievement", saved.getAchievementId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserAchievement by ID
     */
    public Mono<UserAchievementOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserAchievement", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserAchievements
     */
    public Flux<UserAchievementOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserAchievements with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserAchievementOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserAchievement> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_achievement", groupIds);
                            Flux<UserAchievement> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_achievement", groupIds, size, offset);
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
     * Update UserAchievement
     */
    @Transactional
    public Mono<UserAchievementOutputDTO> update(Long id, UserAchievementInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserAchievement", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setTitle(inputDTO.getTitle());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setAchievementType(inputDTO.getAchievementType());
                        existing.setIssuer(inputDTO.getIssuer());
                        existing.setDateAchieved(inputDTO.getDateAchieved());
                        existing.setUrl(inputDTO.getUrl());
                        existing.setDocumentId(inputDTO.getDocumentId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserAchievement", saved.getAchievementId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserAchievement
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserAchievement", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserAchievement", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_achievement", id))
            );
    }
    
    /**
     * Delete UserAchievement with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserAchievement", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserAchievement", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_achievement", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserAchievementOutputDTO toOutputDTO(UserAchievement entity) {
        return UserAchievementOutputDTO.builder()
            .achievementId(entity.getAchievementId())
            .userId(entity.getUserId())
            .title(entity.getTitle())
            .description(entity.getDescription())
            .achievementType(entity.getAchievementType())
            .issuer(entity.getIssuer())
            .dateAchieved(entity.getDateAchieved())
            .url(entity.getUrl())
            .documentId(entity.getDocumentId())
            .build();
    }
}