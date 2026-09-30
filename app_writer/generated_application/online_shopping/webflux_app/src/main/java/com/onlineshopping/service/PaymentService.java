package com.onlineshopping.service;

import com.onlineshopping.entity.Payment;
import com.onlineshopping.dto.PaymentInputDTO;
import com.onlineshopping.dto.PaymentOutputDTO;
import com.onlineshopping.repository.PaymentRepository;
import com.onlineshopping.exception.EntityNotFoundException;
import com.onlineshopping.dto.PageResponse;
import com.onlineshopping.repository.RecordOwnerRepository;
import com.onlineshopping.repository.QueryGroupRecordRepository;
import com.onlineshopping.repository.QueryGroupMemberRepository;
import com.onlineshopping.repository.AuthUserRepository;
import com.onlineshopping.entity.RecordOwner;
import com.onlineshopping.security.SecurityContextHolder;
import com.onlineshopping.auth.JwtService;
import com.onlineshopping.service.ActivityTrackingService;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Service class for Payment business logic.
 */
@Service
@RequiredArgsConstructor
public class PaymentService {
    
    private final PaymentRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new Payment
     */
    @Transactional
    public Mono<PaymentOutputDTO> create(PaymentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                Payment entity = Payment.builder()
                    .orderid(inputDTO.getOrderid())
                    .paymentmethod(inputDTO.getPaymentmethod())
                    .amount(inputDTO.getAmount())
                    .paymentdate(inputDTO.getPaymentdate())
                    .transactionid(inputDTO.getTransactionid())
                    .status(inputDTO.getStatus())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("payment")
                            .recordId(saved.getPaymentId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "Payment", saved.getPaymentId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find Payment by ID
     */
    public Mono<PaymentOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("Payment", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all Payments
     */
    public Flux<PaymentOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find Payments with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<PaymentOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<Payment> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "payment", groupIds);
                            Flux<Payment> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "payment", groupIds, size, offset);
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
     * Update Payment
     */
    @Transactional
    public Mono<PaymentOutputDTO> update(Long id, PaymentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Payment", id)))
                    .flatMap(existing -> {
                        existing.setOrderid(inputDTO.getOrderid());
                        existing.setPaymentmethod(inputDTO.getPaymentmethod());
                        existing.setAmount(inputDTO.getAmount());
                        existing.setPaymentdate(inputDTO.getPaymentdate());
                        existing.setTransactionid(inputDTO.getTransactionid());
                        existing.setStatus(inputDTO.getStatus());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "Payment", saved.getPaymentId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete Payment
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Payment", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Payment", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("payment", id))
            );
    }
    
    /**
     * Delete Payment with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Payment", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Payment", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("payment", id))
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private PaymentOutputDTO toOutputDTO(Payment entity) {
        return PaymentOutputDTO.builder()
            .paymentId(entity.getPaymentId())
            .orderid(entity.getOrderid())
            .paymentmethod(entity.getPaymentmethod())
            .amount(entity.getAmount())
            .paymentdate(entity.getPaymentdate())
            .transactionid(entity.getTransactionid())
            .status(entity.getStatus())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}