package com.onlineshopping.service;

import com.onlineshopping.entity.User;
import com.onlineshopping.dto.UserInputDTO;
import com.onlineshopping.dto.UserOutputDTO;
import com.onlineshopping.repository.UserRepository;
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
 * Service class for User business logic.
 */
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new User
     */
    @Transactional
    public Mono<UserOutputDTO> create(UserInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                User entity = User.builder()
                    .username(inputDTO.getUsername())
                    .encryptedpassword(inputDTO.getEncryptedpassword())
                    .email(inputDTO.getEmail())
                    .firstname(inputDTO.getFirstname())
                    .lastname(inputDTO.getLastname())
                    .phone(inputDTO.getPhone())
                    .role(inputDTO.getRole())
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user")
                            .recordId(saved.getUserId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "User", saved.getUserId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find User by ID
     */
    public Mono<UserOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("User", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all Users
     */
    public Flux<UserOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find Users with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<User> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user", groupIds);
                            Flux<User> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user", groupIds, size, offset);
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
     * Update User
     */
    @Transactional
    public Mono<UserOutputDTO> update(Long id, UserInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("User", id)))
                    .flatMap(existing -> {
                        existing.setUsername(inputDTO.getUsername());
                        existing.setEncryptedpassword(inputDTO.getEncryptedpassword());
                        existing.setEmail(inputDTO.getEmail());
                        existing.setFirstname(inputDTO.getFirstname());
                        existing.setLastname(inputDTO.getLastname());
                        existing.setPhone(inputDTO.getPhone());
                        existing.setRole(inputDTO.getRole());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "User", saved.getUserId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete User
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("User", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "User", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user", id))
            );
    }
    
    /**
     * Delete User with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser(exchange, jwtService, authUserRepository)
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("User", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "User", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user", id))
            );
    }
    

    /**
     * Convert entity to output DTO
     */
    private UserOutputDTO toOutputDTO(User entity) {
        return UserOutputDTO.builder()
            .userId(entity.getUserId())
            .username(entity.getUsername())
            .encryptedpassword(entity.getEncryptedpassword())
            .email(entity.getEmail())
            .firstname(entity.getFirstname())
            .lastname(entity.getLastname())
            .phone(entity.getPhone())
            .role(entity.getRole())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}