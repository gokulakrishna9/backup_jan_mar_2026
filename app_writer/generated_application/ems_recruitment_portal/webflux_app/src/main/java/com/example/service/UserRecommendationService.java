package com.example.service;

import com.example.entity.UserRecommendation;
import com.example.dto.UserRecommendationInputDTO;
import com.example.dto.UserRecommendationOutputDTO;
import com.example.repository.UserRecommendationRepository;
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
 * Service class for UserRecommendation business logic.
 */
@Service
@RequiredArgsConstructor
public class UserRecommendationService {
    
    private final UserRecommendationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserRecommendation
     */
    @Transactional
    public Mono<UserRecommendationOutputDTO> create(UserRecommendationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserRecommendation entity = UserRecommendation.builder()
                    .userId(inputDTO.getUserId())
                    .recommendedByUserId(inputDTO.getRecommendedByUserId())
                    .recommendationText(inputDTO.getRecommendationText())
                    .relationship(inputDTO.getRelationship())
                    .positionAtTime(inputDTO.getPositionAtTime())
                    .isVisible(inputDTO.getIsVisible())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_recommendation")
                            .recordId(saved.getRecommendationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserRecommendation", saved.getRecommendationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserRecommendation by ID
     */
    public Mono<UserRecommendationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserRecommendation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserRecommendations
     */
    public Flux<UserRecommendationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserRecommendations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserRecommendationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserRecommendation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_recommendation", groupIds);
                            Flux<UserRecommendation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_recommendation", groupIds, size, offset);
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
     * Update UserRecommendation
     */
    @Transactional
    public Mono<UserRecommendationOutputDTO> update(Long id, UserRecommendationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserRecommendation", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setRecommendedByUserId(inputDTO.getRecommendedByUserId());
                        existing.setRecommendationText(inputDTO.getRecommendationText());
                        existing.setRelationship(inputDTO.getRelationship());
                        existing.setPositionAtTime(inputDTO.getPositionAtTime());
                        existing.setIsVisible(inputDTO.getIsVisible());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserRecommendation", saved.getRecommendationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserRecommendation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserRecommendation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserRecommendation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_recommendation", id))
            );
    }
    
    /**
     * Delete UserRecommendation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserRecommendation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserRecommendation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_recommendation", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserRecommendationOutputDTO toOutputDTO(UserRecommendation entity) {
        return UserRecommendationOutputDTO.builder()
            .recommendationId(entity.getRecommendationId())
            .userId(entity.getUserId())
            .recommendedByUserId(entity.getRecommendedByUserId())
            .recommendationText(entity.getRecommendationText())
            .relationship(entity.getRelationship())
            .positionAtTime(entity.getPositionAtTime())
            .isVisible(entity.getIsVisible())
            .build();
    }
}