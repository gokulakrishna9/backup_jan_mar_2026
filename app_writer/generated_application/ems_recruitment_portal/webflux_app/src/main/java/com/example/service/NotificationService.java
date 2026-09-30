package com.example.service;

import com.example.entity.Notification;
import com.example.dto.NotificationInputDTO;
import com.example.dto.NotificationOutputDTO;
import com.example.repository.NotificationRepository;
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
 * Service class for Notification business logic.
 */
@Service
@RequiredArgsConstructor
public class NotificationService {
    
    private final NotificationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new Notification
     */
    @Transactional
    public Mono<NotificationOutputDTO> create(NotificationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                Notification entity = Notification.builder()
                    .userId(inputDTO.getUserId())
                    .notificationType(inputDTO.getNotificationType())
                    .title(inputDTO.getTitle())
                    .message(inputDTO.getMessage())
                    .relatedEntityType(inputDTO.getRelatedEntityType())
                    .relatedEntityId(inputDTO.getRelatedEntityId())
                    .actionUrl(inputDTO.getActionUrl())
                    .isRead(inputDTO.getIsRead())
                    .readAt(inputDTO.getReadAt())
                    .priority(inputDTO.getPriority())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("notification")
                            .recordId(saved.getNotificationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "Notification", saved.getNotificationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find Notification by ID
     */
    public Mono<NotificationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("Notification", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all Notifications
     */
    public Flux<NotificationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find Notifications with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<NotificationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<Notification> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "notification", groupIds);
                            Flux<Notification> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "notification", groupIds, size, offset);
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
     * Update Notification
     */
    @Transactional
    public Mono<NotificationOutputDTO> update(Long id, NotificationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Notification", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setNotificationType(inputDTO.getNotificationType());
                        existing.setTitle(inputDTO.getTitle());
                        existing.setMessage(inputDTO.getMessage());
                        existing.setRelatedEntityType(inputDTO.getRelatedEntityType());
                        existing.setRelatedEntityId(inputDTO.getRelatedEntityId());
                        existing.setActionUrl(inputDTO.getActionUrl());
                        existing.setIsRead(inputDTO.getIsRead());
                        existing.setReadAt(inputDTO.getReadAt());
                        existing.setPriority(inputDTO.getPriority());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "Notification", saved.getNotificationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete Notification
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Notification", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Notification", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("notification", id))
            );
    }
    
    /**
     * Delete Notification with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("Notification", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "Notification", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("notification", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private NotificationOutputDTO toOutputDTO(Notification entity) {
        return NotificationOutputDTO.builder()
            .notificationId(entity.getNotificationId())
            .userId(entity.getUserId())
            .notificationType(entity.getNotificationType())
            .title(entity.getTitle())
            .message(entity.getMessage())
            .relatedEntityType(entity.getRelatedEntityType())
            .relatedEntityId(entity.getRelatedEntityId())
            .actionUrl(entity.getActionUrl())
            .isRead(entity.getIsRead())
            .readAt(entity.getReadAt())
            .priority(entity.getPriority())
            .build();
    }
}