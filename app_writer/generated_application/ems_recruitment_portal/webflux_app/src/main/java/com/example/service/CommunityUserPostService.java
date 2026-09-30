package com.example.service;

import com.example.entity.CommunityUserPost;
import com.example.dto.CommunityUserPostInputDTO;
import com.example.dto.CommunityUserPostOutputDTO;
import com.example.repository.CommunityUserPostRepository;
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
 * Service class for CommunityUserPost business logic.
 */
@Service
@RequiredArgsConstructor
public class CommunityUserPostService {
    
    private final CommunityUserPostRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CommunityUserPost
     */
    @Transactional
    public Mono<CommunityUserPostOutputDTO> create(CommunityUserPostInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CommunityUserPost entity = CommunityUserPost.builder()
                    .communityId(inputDTO.getCommunityId())
                    .userId(inputDTO.getUserId())
                    .post(inputDTO.getPost())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("community_user_post")
                            .recordId(saved.getPostId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityUserPost", saved.getPostId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CommunityUserPost by ID
     */
    public Mono<CommunityUserPostOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityUserPost", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CommunityUserPosts
     */
    public Flux<CommunityUserPostOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CommunityUserPosts with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CommunityUserPostOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CommunityUserPost> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "community_user_post", groupIds);
                            Flux<CommunityUserPost> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "community_user_post", groupIds, size, offset);
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
     * Update CommunityUserPost
     */
    @Transactional
    public Mono<CommunityUserPostOutputDTO> update(Long id, CommunityUserPostInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityUserPost", id)))
                    .flatMap(existing -> {
                        existing.setCommunityId(inputDTO.getCommunityId());
                        existing.setUserId(inputDTO.getUserId());
                        existing.setPost(inputDTO.getPost());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityUserPost", saved.getPostId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CommunityUserPost
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityUserPost", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityUserPost", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_user_post", id))
            );
    }
    
    /**
     * Delete CommunityUserPost with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityUserPost", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityUserPost", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_user_post", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CommunityUserPostOutputDTO toOutputDTO(CommunityUserPost entity) {
        return CommunityUserPostOutputDTO.builder()
            .postId(entity.getPostId())
            .communityId(entity.getCommunityId())
            .userId(entity.getUserId())
            .post(entity.getPost())
            .build();
    }
}