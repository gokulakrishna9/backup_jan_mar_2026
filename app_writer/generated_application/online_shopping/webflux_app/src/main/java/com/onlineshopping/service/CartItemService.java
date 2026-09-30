package com.onlineshopping.service;

import com.onlineshopping.entity.CartItem;
import com.onlineshopping.dto.CartItemInputDTO;
import com.onlineshopping.dto.CartItemOutputDTO;
import com.onlineshopping.repository.CartItemRepository;
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
 * Service class for CartItem business logic.
 */
@Service
@RequiredArgsConstructor
public class CartItemService {
    
    private final CartItemRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CartItem
     */
    @Transactional
    public Mono<CartItemOutputDTO> create(CartItemInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CartItem entity = CartItem.builder()
                    .cartid(inputDTO.getCartid())
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
                            .tableName("cart_item")
                            .recordId(saved.getCartItemId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CartItem", saved.getCartItemId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CartItem by ID
     */
    public Mono<CartItemOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CartItem", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CartItems
     */
    public Flux<CartItemOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CartItems with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CartItemOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CartItem> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "cart_item", groupIds);
                            Flux<CartItem> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "cart_item", groupIds, size, offset);
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
     * Update CartItem
     */
    @Transactional
    public Mono<CartItemOutputDTO> update(Long id, CartItemInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CartItem", id)))
                    .flatMap(existing -> {
                        existing.setCartid(inputDTO.getCartid());
                        existing.setProductid(inputDTO.getProductid());
                        existing.setQuantity(inputDTO.getQuantity());
                        existing.setUnitprice(inputDTO.getUnitprice());
                        existing.setSubtotal(inputDTO.getSubtotal());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CartItem", saved.getCartItemId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CartItem
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CartItem", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CartItem", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("cart_item", id))
            );
    }
    
    /**
     * Delete CartItem with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CartItem", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CartItem", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("cart_item", id))
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private CartItemOutputDTO toOutputDTO(CartItem entity) {
        return CartItemOutputDTO.builder()
            .cartItemId(entity.getCartItemId())
            .cartid(entity.getCartid())
            .productid(entity.getProductid())
            .quantity(entity.getQuantity())
            .unitprice(entity.getUnitprice())
            .subtotal(entity.getSubtotal())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}