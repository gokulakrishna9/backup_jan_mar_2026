package com.example.service;

import com.example.entity.User;
import com.example.dto.UserInputDTO;
import com.example.dto.UserOutputDTO;
import com.example.repository.UserRepository;
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
 * Service class for User business logic.
 */
@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new User
     */
    @Transactional
    public Mono<UserOutputDTO> create(UserInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                User entity = User.builder()
                    .firstName(inputDTO.getFirstName())
                    .lastName(inputDTO.getLastName())
                    .gender(inputDTO.getGender())
                    .dateOfBirth(inputDTO.getDateOfBirth())
                    .emailAddress(inputDTO.getEmailAddress())
                    .userName(inputDTO.getUserName())
                    .encryptedPassword(inputDTO.getEncryptedPassword())
                    .phoneNumber(inputDTO.getPhoneNumber())
                    .profilePhoto(inputDTO.getProfilePhoto())
                    .isActive(inputDTO.getIsActive())
                    .isEntity(inputDTO.getIsEntity())
                    .isPublic(inputDTO.getIsPublic())
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
                        existing.setFirstName(inputDTO.getFirstName());
                        existing.setLastName(inputDTO.getLastName());
                        existing.setGender(inputDTO.getGender());
                        existing.setDateOfBirth(inputDTO.getDateOfBirth());
                        existing.setEmailAddress(inputDTO.getEmailAddress());
                        existing.setUserName(inputDTO.getUserName());
                        existing.setEncryptedPassword(inputDTO.getEncryptedPassword());
                        existing.setPhoneNumber(inputDTO.getPhoneNumber());
                        existing.setProfilePhoto(inputDTO.getProfilePhoto());
                        existing.setIsActive(inputDTO.getIsActive());
                        existing.setIsEntity(inputDTO.getIsEntity());
                        existing.setIsPublic(inputDTO.getIsPublic());
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
        return SecurityContextHolder.getCurrentUser()
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
        return SecurityContextHolder.getCurrentUser()
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
            .firstName(entity.getFirstName())
            .lastName(entity.getLastName())
            .gender(entity.getGender())
            .dateOfBirth(entity.getDateOfBirth())
            .emailAddress(entity.getEmailAddress())
            .userName(entity.getUserName())
            .phoneNumber(entity.getPhoneNumber())
            .profilePhoto(entity.getProfilePhoto())
            .isActive(entity.getIsActive())
            .isEntity(entity.getIsEntity())
            .isPublic(entity.getIsPublic())
            .build();
    }
}