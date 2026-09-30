package com.onlineshopping.service;

import com.onlineshopping.entity.OrderItem;
import com.onlineshopping.dto.OrderItemInputDTO;
import com.onlineshopping.dto.OrderItemOutputDTO;
import com.onlineshopping.repository.OrderItemRepository;
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
 * Service class for OrderItem business logic.
 */
@Service
@RequiredArgsConstructor
public class OrderItemService {
    
    private final OrderItemRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new OrderItem
     */
    @Transactional
    public Mono<OrderItemOutputDTO> create(OrderItemInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                OrderItem entity = OrderItem.builder()
                    .orderid(inputDTO.getOrderid())
                    .productid(inputDTO.getProductid())
                    .quantity(inputDTO.getQuantity())
                    .unitprice(inputDTO.getUnitprice())
                    .subtotal(inputDTO.getSubtotal())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("order_item")
                            .recordId(saved.getOrderItemId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "OrderItem", saved.getOrderItemId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find OrderItem by ID
     */
    public Mono<OrderItemOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("OrderItem", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all OrderItems
     */
    public Flux<OrderItemOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find OrderItems with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<OrderItemOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<OrderItem> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "order_item", groupIds);
                            Flux<OrderItem> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "order_item", groupIds, size, offset);
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
     * Update OrderItem
     */
    @Transactional
    public Mono<OrderItemOutputDTO> update(Long id, OrderItemInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("OrderItem", id)))
                    .flatMap(existing -> {
                        existing.setOrderid(inputDTO.getOrderid());
                        existing.setProductid(inputDTO.getProductid());
                        existing.setQuantity(inputDTO.getQuantity());
                        existing.setUnitprice(inputDTO.getUnitprice());
                        existing.setSubtotal(inputDTO.getSubtotal());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "OrderItem", saved.getOrderItemId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete OrderItem
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("OrderItem", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "OrderItem", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("order_item", id))
            );
    }
    
    /**
     * Delete OrderItem with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("OrderItem", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "OrderItem", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("order_item", id))
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private OrderItemOutputDTO toOutputDTO(OrderItem entity) {
        return OrderItemOutputDTO.builder()
            .orderItemId(entity.getOrderItemId())
            .orderid(entity.getOrderid())
            .productid(entity.getProductid())
            .quantity(entity.getQuantity())
            .unitprice(entity.getUnitprice())
            .subtotal(entity.getSubtotal())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}