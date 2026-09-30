package com.example.service;

import com.example.entity.PostCommentEmogiLink;
import com.example.dto.PostCommentEmogiLinkInputDTO;
import com.example.dto.PostCommentEmogiLinkOutputDTO;
import com.example.repository.PostCommentEmogiLinkRepository;
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
 * Service class for PostCommentEmogiLink business logic.
 */
@Service
@RequiredArgsConstructor
public class PostCommentEmogiLinkService {
    
    private final PostCommentEmogiLinkRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new PostCommentEmogiLink
     */
    @Transactional
    public Mono<PostCommentEmogiLinkOutputDTO> create(PostCommentEmogiLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                PostCommentEmogiLink entity = PostCommentEmogiLink.builder()
                    .commentId(inputDTO.getCommentId())
                    .emogiId(inputDTO.getEmogiId())
                    .userId(inputDTO.getUserId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("post_comment_emogi_link")
                            .recordId(saved.getLinkId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "PostCommentEmogiLink", saved.getLinkId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find PostCommentEmogiLink by ID
     */
    public Mono<PostCommentEmogiLinkOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("PostCommentEmogiLink", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all PostCommentEmogiLinks
     */
    public Flux<PostCommentEmogiLinkOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find PostCommentEmogiLinks with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<PostCommentEmogiLinkOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<PostCommentEmogiLink> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "post_comment_emogi_link", groupIds);
                            Flux<PostCommentEmogiLink> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "post_comment_emogi_link", groupIds, size, offset);
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
     * Update PostCommentEmogiLink
     */
    @Transactional
    public Mono<PostCommentEmogiLinkOutputDTO> update(Long id, PostCommentEmogiLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("PostCommentEmogiLink", id)))
                    .flatMap(existing -> {
                        existing.setCommentId(inputDTO.getCommentId());
                        existing.setEmogiId(inputDTO.getEmogiId());
                        existing.setUserId(inputDTO.getUserId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "PostCommentEmogiLink", saved.getLinkId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete PostCommentEmogiLink
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("PostCommentEmogiLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "PostCommentEmogiLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("post_comment_emogi_link", id))
            );
    }
    
    /**
     * Delete PostCommentEmogiLink with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("PostCommentEmogiLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "PostCommentEmogiLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("post_comment_emogi_link", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private PostCommentEmogiLinkOutputDTO toOutputDTO(PostCommentEmogiLink entity) {
        return PostCommentEmogiLinkOutputDTO.builder()
            .linkId(entity.getLinkId())
            .commentId(entity.getCommentId())
            .emogiId(entity.getEmogiId())
            .userId(entity.getUserId())
            .build();
    }
}