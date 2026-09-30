package com.example.service;

import com.example.entity.CommunityCategory;
import com.example.dto.CommunityCategoryInputDTO;
import com.example.dto.CommunityCategoryOutputDTO;
import com.example.repository.CommunityCategoryRepository;
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
 * Service class for CommunityCategory business logic.
 */
@Service
@RequiredArgsConstructor
public class CommunityCategoryService {
    
    private final CommunityCategoryRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CommunityCategory
     */
    @Transactional
    public Mono<CommunityCategoryOutputDTO> create(CommunityCategoryInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CommunityCategory entity = CommunityCategory.builder()
                    .communityId(inputDTO.getCommunityId())
                    .categoryName(inputDTO.getCategoryName())
                    .description(inputDTO.getDescription())
                    .icon(inputDTO.getIcon())
                    .color(inputDTO.getColor())
                    .orderSequence(inputDTO.getOrderSequence())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("community_category")
                            .recordId(saved.getCategoryId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityCategory", saved.getCategoryId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CommunityCategory by ID
     */
    public Mono<CommunityCategoryOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityCategory", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CommunityCategorys
     */
    public Flux<CommunityCategoryOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CommunityCategorys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CommunityCategoryOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CommunityCategory> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "community_category", groupIds);
                            Flux<CommunityCategory> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "community_category", groupIds, size, offset);
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
     * Update CommunityCategory
     */
    @Transactional
    public Mono<CommunityCategoryOutputDTO> update(Long id, CommunityCategoryInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityCategory", id)))
                    .flatMap(existing -> {
                        existing.setCommunityId(inputDTO.getCommunityId());
                        existing.setCategoryName(inputDTO.getCategoryName());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setIcon(inputDTO.getIcon());
                        existing.setColor(inputDTO.getColor());
                        existing.setOrderSequence(inputDTO.getOrderSequence());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityCategory", saved.getCategoryId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CommunityCategory
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityCategory", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityCategory", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_category", id))
            );
    }
    
    /**
     * Delete CommunityCategory with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityCategory", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityCategory", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_category", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CommunityCategoryOutputDTO toOutputDTO(CommunityCategory entity) {
        return CommunityCategoryOutputDTO.builder()
            .categoryId(entity.getCategoryId())
            .communityId(entity.getCommunityId())
            .categoryName(entity.getCategoryName())
            .description(entity.getDescription())
            .icon(entity.getIcon())
            .color(entity.getColor())
            .orderSequence(entity.getOrderSequence())
            .build();
    }
}