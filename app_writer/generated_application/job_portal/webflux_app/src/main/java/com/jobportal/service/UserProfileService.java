package com.jobportal.service;

import com.jobportal.entity.UserProfile;
import com.jobportal.dto.UserProfileInputDTO;
import com.jobportal.dto.UserProfileOutputDTO;
import com.jobportal.repository.UserProfileRepository;
import com.jobportal.exception.EntityNotFoundException;
import com.jobportal.dto.PageResponse;
import com.jobportal.repository.RecordOwnerRepository;
import com.jobportal.repository.QueryGroupRecordRepository;
import com.jobportal.repository.QueryGroupMemberRepository;
import com.jobportal.repository.AuthUserRepository;
import com.jobportal.entity.RecordOwner;
import com.jobportal.security.SecurityContextHolder;
import com.jobportal.auth.JwtService;
import com.jobportal.service.ActivityTrackingService;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Service class for UserProfile business logic.
 */
@Service
@RequiredArgsConstructor
public class UserProfileService {
    
    private final UserProfileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserProfile
     */
    @Transactional
    public Mono<UserProfileOutputDTO> create(UserProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                // Single-record-per-user: reject if user already owns a record
                return repository.findByOwnerUserId(user.getAuthUserId())
                    .flatMap(existing -> Mono.<UserProfile>error(
                        new IllegalStateException("UserProfile: only one record per user is allowed")))
                    .switchIfEmpty(Mono.defer(() -> {
                        UserProfile entity = UserProfile.builder()
                            .firstname(inputDTO.getFirstname())
                            .lastname(inputDTO.getLastname())
                            .email(inputDTO.getEmail())
                            .phone(inputDTO.getPhone())
                            .bio(inputDTO.getBio())
                            .createdAt(LocalDateTime.now())
                            .updatedAt(LocalDateTime.now())
                            .build();
                        
                        return repository.save(entity)
                            .flatMap(saved -> {
                                RecordOwner recordOwner = RecordOwner.builder()
                                    .authUserId(user.getAuthUserId())
                                    .tableName("user_profile")
                                    .recordId(saved.getUserProfileId())
                                    .createdAt(LocalDateTime.now())
                                    .build();
                                return recordOwnerRepository.save(recordOwner)
                                    .thenReturn(saved);
                            });
                    }))
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProfile", saved.getUserProfileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserProfile by ID
     */
    public Mono<UserProfileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProfile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserProfiles
     */
    public Flux<UserProfileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserProfiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserProfileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserProfile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_profile", groupIds);
                            Flux<UserProfile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_profile", groupIds, size, offset);
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
     * Update UserProfile
     */
    @Transactional
    public Mono<UserProfileOutputDTO> update(Long id, UserProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProfile", id)))
                    .flatMap(existing -> {
                        existing.setFirstname(inputDTO.getFirstname());
                        existing.setLastname(inputDTO.getLastname());
                        existing.setEmail(inputDTO.getEmail());
                        existing.setPhone(inputDTO.getPhone());
                        existing.setBio(inputDTO.getBio());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProfile", saved.getUserProfileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserProfile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProfile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProfile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_profile", id))
                    .then()
            );
    }
    
    /**
     * Delete UserProfile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserProfile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserProfile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_profile", id))
                    .then()
            );
    }
    
    /**
     * Find the current user's own UserProfile record (single-record-per-user).
     */
    public Mono<UserProfileOutputDTO> findMyRecord() {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> repository.findByOwnerUserId(user.getAuthUserId()))
            .map(this::toOutputDTO);
    }

    /**
     * Convert entity to output DTO
     */
    private UserProfileOutputDTO toOutputDTO(UserProfile entity) {
        return UserProfileOutputDTO.builder()
            .userProfileId(entity.getUserProfileId())
            .firstname(entity.getFirstname())
            .lastname(entity.getLastname())
            .email(entity.getEmail())
            .phone(entity.getPhone())
            .bio(entity.getBio())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}