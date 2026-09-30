package com.example.service;

import com.example.entity.CourseReview;
import com.example.dto.CourseReviewInputDTO;
import com.example.dto.CourseReviewOutputDTO;
import com.example.repository.CourseReviewRepository;
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
 * Service class for CourseReview business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseReviewService {
    
    private final CourseReviewRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseReview
     */
    @Transactional
    public Mono<CourseReviewOutputDTO> create(CourseReviewInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseReview entity = CourseReview.builder()
                    .courseId(inputDTO.getCourseId())
                    .userId(inputDTO.getUserId())
                    .rating(inputDTO.getRating())
                    .reviewTitle(inputDTO.getReviewTitle())
                    .reviewText(inputDTO.getReviewText())
                    .helpfulCount(inputDTO.getHelpfulCount())
                    .isVerifiedPurchase(inputDTO.getIsVerifiedPurchase())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_review")
                            .recordId(saved.getReviewId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseReview", saved.getReviewId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseReview by ID
     */
    public Mono<CourseReviewOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseReview", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseReviews
     */
    public Flux<CourseReviewOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseReviews with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseReviewOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseReview> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_review", groupIds);
                            Flux<CourseReview> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_review", groupIds, size, offset);
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
     * Update CourseReview
     */
    @Transactional
    public Mono<CourseReviewOutputDTO> update(Long id, CourseReviewInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseReview", id)))
                    .flatMap(existing -> {
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setUserId(inputDTO.getUserId());
                        existing.setRating(inputDTO.getRating());
                        existing.setReviewTitle(inputDTO.getReviewTitle());
                        existing.setReviewText(inputDTO.getReviewText());
                        existing.setHelpfulCount(inputDTO.getHelpfulCount());
                        existing.setIsVerifiedPurchase(inputDTO.getIsVerifiedPurchase());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseReview", saved.getReviewId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseReview
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseReview", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseReview", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_review", id))
            );
    }
    
    /**
     * Delete CourseReview with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseReview", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseReview", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_review", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CourseReviewOutputDTO toOutputDTO(CourseReview entity) {
        return CourseReviewOutputDTO.builder()
            .reviewId(entity.getReviewId())
            .courseId(entity.getCourseId())
            .userId(entity.getUserId())
            .rating(entity.getRating())
            .reviewTitle(entity.getReviewTitle())
            .reviewText(entity.getReviewText())
            .helpfulCount(entity.getHelpfulCount())
            .isVerifiedPurchase(entity.getIsVerifiedPurchase())
            .build();
    }
}