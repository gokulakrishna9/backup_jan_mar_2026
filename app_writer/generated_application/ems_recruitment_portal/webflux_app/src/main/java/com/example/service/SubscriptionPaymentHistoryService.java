package com.example.service;

import com.example.entity.SubscriptionPaymentHistory;
import com.example.dto.SubscriptionPaymentHistoryInputDTO;
import com.example.dto.SubscriptionPaymentHistoryOutputDTO;
import com.example.repository.SubscriptionPaymentHistoryRepository;
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
 * Service class for SubscriptionPaymentHistory business logic.
 */
@Service
@RequiredArgsConstructor
public class SubscriptionPaymentHistoryService {
    
    private final SubscriptionPaymentHistoryRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new SubscriptionPaymentHistory
     */
    @Transactional
    public Mono<SubscriptionPaymentHistoryOutputDTO> create(SubscriptionPaymentHistoryInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                SubscriptionPaymentHistory entity = SubscriptionPaymentHistory.builder()
                    .userId(inputDTO.getUserId())
                    .amount(inputDTO.getAmount())
                    .subscriptionType(inputDTO.getSubscriptionType())
                    .transactionDetails(inputDTO.getTransactionDetails())
                    .transactionReference(inputDTO.getTransactionReference())
                    .paymentOn(inputDTO.getPaymentOn())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("subscription_payment_history")
                            .recordId(saved.getPaymentId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "SubscriptionPaymentHistory", saved.getPaymentId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find SubscriptionPaymentHistory by ID
     */
    public Mono<SubscriptionPaymentHistoryOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("SubscriptionPaymentHistory", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all SubscriptionPaymentHistorys
     */
    public Flux<SubscriptionPaymentHistoryOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find SubscriptionPaymentHistorys with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<SubscriptionPaymentHistoryOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<SubscriptionPaymentHistory> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "subscription_payment_history", groupIds);
                            Flux<SubscriptionPaymentHistory> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "subscription_payment_history", groupIds, size, offset);
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
     * Update SubscriptionPaymentHistory
     */
    @Transactional
    public Mono<SubscriptionPaymentHistoryOutputDTO> update(Long id, SubscriptionPaymentHistoryInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("SubscriptionPaymentHistory", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setAmount(inputDTO.getAmount());
                        existing.setSubscriptionType(inputDTO.getSubscriptionType());
                        existing.setTransactionDetails(inputDTO.getTransactionDetails());
                        existing.setTransactionReference(inputDTO.getTransactionReference());
                        existing.setPaymentOn(inputDTO.getPaymentOn());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "SubscriptionPaymentHistory", saved.getPaymentId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete SubscriptionPaymentHistory
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("SubscriptionPaymentHistory", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "SubscriptionPaymentHistory", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("subscription_payment_history", id))
            );
    }
    
    /**
     * Delete SubscriptionPaymentHistory with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("SubscriptionPaymentHistory", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "SubscriptionPaymentHistory", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("subscription_payment_history", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private SubscriptionPaymentHistoryOutputDTO toOutputDTO(SubscriptionPaymentHistory entity) {
        return SubscriptionPaymentHistoryOutputDTO.builder()
            .paymentId(entity.getPaymentId())
            .userId(entity.getUserId())
            .amount(entity.getAmount())
            .subscriptionType(entity.getSubscriptionType())
            .transactionDetails(entity.getTransactionDetails())
            .transactionReference(entity.getTransactionReference())
            .paymentOn(entity.getPaymentOn())
            .build();
    }
}