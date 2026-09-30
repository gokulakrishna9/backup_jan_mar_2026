package com.example.service;

import com.example.entity.UserCoursePurchase;
import com.example.dto.UserCoursePurchaseInputDTO;
import com.example.dto.UserCoursePurchaseOutputDTO;
import com.example.repository.UserCoursePurchaseRepository;
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
 * Service class for UserCoursePurchase business logic.
 */
@Service
@RequiredArgsConstructor
public class UserCoursePurchaseService {
    
    private final UserCoursePurchaseRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserCoursePurchase
     */
    @Transactional
    public Mono<UserCoursePurchaseOutputDTO> create(UserCoursePurchaseInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserCoursePurchase entity = UserCoursePurchase.builder()
                    .userId(inputDTO.getUserId())
                    .courseId(inputDTO.getCourseId())
                    .comment(inputDTO.getComment())
                    .amount(inputDTO.getAmount())
                    .transactionId(inputDTO.getTransactionId())
                    .purchasedOn(inputDTO.getPurchasedOn())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_course_purchase")
                            .recordId(saved.getPurchaseId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCoursePurchase", saved.getPurchaseId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserCoursePurchase by ID
     */
    public Mono<UserCoursePurchaseOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCoursePurchase", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserCoursePurchases
     */
    public Flux<UserCoursePurchaseOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserCoursePurchases with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserCoursePurchaseOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserCoursePurchase> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_course_purchase", groupIds);
                            Flux<UserCoursePurchase> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_course_purchase", groupIds, size, offset);
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
     * Update UserCoursePurchase
     */
    @Transactional
    public Mono<UserCoursePurchaseOutputDTO> update(Long id, UserCoursePurchaseInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCoursePurchase", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setComment(inputDTO.getComment());
                        existing.setAmount(inputDTO.getAmount());
                        existing.setTransactionId(inputDTO.getTransactionId());
                        existing.setPurchasedOn(inputDTO.getPurchasedOn());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCoursePurchase", saved.getPurchaseId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserCoursePurchase
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCoursePurchase", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCoursePurchase", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_course_purchase", id))
            );
    }
    
    /**
     * Delete UserCoursePurchase with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserCoursePurchase", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserCoursePurchase", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_course_purchase", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserCoursePurchaseOutputDTO toOutputDTO(UserCoursePurchase entity) {
        return UserCoursePurchaseOutputDTO.builder()
            .purchaseId(entity.getPurchaseId())
            .userId(entity.getUserId())
            .courseId(entity.getCourseId())
            .comment(entity.getComment())
            .amount(entity.getAmount())
            .transactionId(entity.getTransactionId())
            .purchasedOn(entity.getPurchasedOn())
            .build();
    }
}