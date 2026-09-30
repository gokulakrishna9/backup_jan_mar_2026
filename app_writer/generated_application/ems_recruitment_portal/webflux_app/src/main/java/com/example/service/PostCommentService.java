package com.example.service;

import com.example.entity.PostComment;
import com.example.dto.PostCommentInputDTO;
import com.example.dto.PostCommentOutputDTO;
import com.example.repository.PostCommentRepository;
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
 * Service class for PostComment business logic.
 */
@Service
@RequiredArgsConstructor
public class PostCommentService {
    
    private final PostCommentRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new PostComment
     */
    @Transactional
    public Mono<PostCommentOutputDTO> create(PostCommentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                PostComment entity = PostComment.builder()
                    .postId(inputDTO.getPostId())
                    .comment(inputDTO.getComment())
                    .userId(inputDTO.getUserId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("post_comment")
                            .recordId(saved.getCommentId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "PostComment", saved.getCommentId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find PostComment by ID
     */
    public Mono<PostCommentOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("PostComment", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all PostComments
     */
    public Flux<PostCommentOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find PostComments with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<PostCommentOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<PostComment> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "post_comment", groupIds);
                            Flux<PostComment> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "post_comment", groupIds, size, offset);
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
     * Update PostComment
     */
    @Transactional
    public Mono<PostCommentOutputDTO> update(Long id, PostCommentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("PostComment", id)))
                    .flatMap(existing -> {
                        existing.setPostId(inputDTO.getPostId());
                        existing.setComment(inputDTO.getComment());
                        existing.setUserId(inputDTO.getUserId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "PostComment", saved.getCommentId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete PostComment
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("PostComment", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "PostComment", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("post_comment", id))
            );
    }
    
    /**
     * Delete PostComment with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("PostComment", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "PostComment", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("post_comment", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private PostCommentOutputDTO toOutputDTO(PostComment entity) {
        return PostCommentOutputDTO.builder()
            .commentId(entity.getCommentId())
            .postId(entity.getPostId())
            .comment(entity.getComment())
            .userId(entity.getUserId())
            .build();
    }
}