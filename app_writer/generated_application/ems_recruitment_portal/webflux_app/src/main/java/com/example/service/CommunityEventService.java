package com.example.service;

import com.example.entity.CommunityEvent;
import com.example.dto.CommunityEventInputDTO;
import com.example.dto.CommunityEventOutputDTO;
import com.example.repository.CommunityEventRepository;
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
 * Service class for CommunityEvent business logic.
 */
@Service
@RequiredArgsConstructor
public class CommunityEventService {
    
    private final CommunityEventRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CommunityEvent
     */
    @Transactional
    public Mono<CommunityEventOutputDTO> create(CommunityEventInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CommunityEvent entity = CommunityEvent.builder()
                    .communityId(inputDTO.getCommunityId())
                    .eventTitle(inputDTO.getEventTitle())
                    .description(inputDTO.getDescription())
                    .eventType(inputDTO.getEventType())
                    .startDatetime(inputDTO.getStartDatetime())
                    .endDatetime(inputDTO.getEndDatetime())
                    .location(inputDTO.getLocation())
                    .meetingLink(inputDTO.getMeetingLink())
                    .maxAttendees(inputDTO.getMaxAttendees())
                    .organizerUserId(inputDTO.getOrganizerUserId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("community_event")
                            .recordId(saved.getEventId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityEvent", saved.getEventId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CommunityEvent by ID
     */
    public Mono<CommunityEventOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityEvent", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CommunityEvents
     */
    public Flux<CommunityEventOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CommunityEvents with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CommunityEventOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CommunityEvent> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "community_event", groupIds);
                            Flux<CommunityEvent> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "community_event", groupIds, size, offset);
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
     * Update CommunityEvent
     */
    @Transactional
    public Mono<CommunityEventOutputDTO> update(Long id, CommunityEventInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityEvent", id)))
                    .flatMap(existing -> {
                        existing.setCommunityId(inputDTO.getCommunityId());
                        existing.setEventTitle(inputDTO.getEventTitle());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setEventType(inputDTO.getEventType());
                        existing.setStartDatetime(inputDTO.getStartDatetime());
                        existing.setEndDatetime(inputDTO.getEndDatetime());
                        existing.setLocation(inputDTO.getLocation());
                        existing.setMeetingLink(inputDTO.getMeetingLink());
                        existing.setMaxAttendees(inputDTO.getMaxAttendees());
                        existing.setOrganizerUserId(inputDTO.getOrganizerUserId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityEvent", saved.getEventId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CommunityEvent
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityEvent", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityEvent", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_event", id))
            );
    }
    
    /**
     * Delete CommunityEvent with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityEvent", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityEvent", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_event", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CommunityEventOutputDTO toOutputDTO(CommunityEvent entity) {
        return CommunityEventOutputDTO.builder()
            .eventId(entity.getEventId())
            .communityId(entity.getCommunityId())
            .eventTitle(entity.getEventTitle())
            .description(entity.getDescription())
            .eventType(entity.getEventType())
            .startDatetime(entity.getStartDatetime())
            .endDatetime(entity.getEndDatetime())
            .location(entity.getLocation())
            .meetingLink(entity.getMeetingLink())
            .maxAttendees(entity.getMaxAttendees())
            .organizerUserId(entity.getOrganizerUserId())
            .build();
    }
}