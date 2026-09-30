package com.onlineshopping.service;

import com.onlineshopping.entity.Order;
import com.onlineshopping.dto.OrderInputDTO;
import com.onlineshopping.dto.OrderOutputDTO;
import com.onlineshopping.repository.OrderRepository;
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
 * Service class for Order business logic.
 */
@Service
@RequiredArgsConstructor
public class OrderService {
    
    private final OrderRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new Order
     */
    @Transactional
    public Mono<OrderOutputDTO> create(OrderInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                Order entity = Order.builder()
                    .userid(inputDTO.getUserid())
                    .orderdate(inputDTO.getOrderdate())
                    .status(inputDTO.getStatus())
                    .totalamount(inputDTO.getTotalamount())
                    .shippingaddressid(inputDTO.getShippingaddressid())
                    .trackingnumber(inputDTO.getTrackingnumber())
                    .notes(inputDTO.getNotes())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("order")
                            .recordId(saved.getOrderId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "Order", saved.getOrderId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find Order by ID
     */
    public Mono<OrderOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("Order", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all Orders
     */
    public Flux<OrderOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find Orders with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<OrderOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<Order> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "order", groupIds);
                            Flux<Order> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "order", groupIds, size, offset);
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
     * Update Order
     */
    @Transactional
    public Mono<OrderOutputDTO> update(Long id, OrderInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Order", id)))
                    .flatMap(existing -> {
                        existing.setUserid(inputDTO.getUserid());
                        existing.setOrderdate(inputDTO.getOrderdate());
                        existing.setStatus(inputDTO.getStatus());
                        existing.setTotalamount(inputDTO.getTotalamount());
                        existing.setShippingaddressid(inputDTO.getShippingaddressid());
                        existing.setTrackingnumber(inputDTO.getTrackingnumber());
                        existing.setNotes(inputDTO.getNotes());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "Order", saved.getOrderId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete Order
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Order", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Order", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("order", id))
            );
    }
    
    /**
     * Delete Order with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Order", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Order", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("order", id))
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private OrderOutputDTO toOutputDTO(Order entity) {
        return OrderOutputDTO.builder()
            .orderId(entity.getOrderId())
            .userid(entity.getUserid())
            .orderdate(entity.getOrderdate())
            .status(entity.getStatus())
            .totalamount(entity.getTotalamount())
            .shippingaddressid(entity.getShippingaddressid())
            .trackingnumber(entity.getTrackingnumber())
            .notes(entity.getNotes())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}