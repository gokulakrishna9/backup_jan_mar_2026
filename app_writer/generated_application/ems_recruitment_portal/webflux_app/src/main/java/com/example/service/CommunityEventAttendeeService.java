package com.example.service;

import com.example.entity.CommunityEventAttendee;
import com.example.dto.CommunityEventAttendeeInputDTO;
import com.example.dto.CommunityEventAttendeeOutputDTO;
import com.example.repository.CommunityEventAttendeeRepository;
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
 * Service class for CommunityEventAttendee business logic.
 */
@Service
@RequiredArgsConstructor
public class CommunityEventAttendeeService {
    
    private final CommunityEventAttendeeRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CommunityEventAttendee
     */
    @Transactional
    public Mono<CommunityEventAttendeeOutputDTO> create(CommunityEventAttendeeInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CommunityEventAttendee entity = CommunityEventAttendee.builder()
                    .eventId(inputDTO.getEventId())
                    .userId(inputDTO.getUserId())
                    .rsvpStatus(inputDTO.getRsvpStatus())
                    .attended(inputDTO.getAttended())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("community_event_attendee")
                            .recordId(saved.getAttendeeId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityEventAttendee", saved.getAttendeeId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CommunityEventAttendee by ID
     */
    public Mono<CommunityEventAttendeeOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityEventAttendee", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CommunityEventAttendees
     */
    public Flux<CommunityEventAttendeeOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CommunityEventAttendees with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CommunityEventAttendeeOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CommunityEventAttendee> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "community_event_attendee", groupIds);
                            Flux<CommunityEventAttendee> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "community_event_attendee", groupIds, size, offset);
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
     * Update CommunityEventAttendee
     */
    @Transactional
    public Mono<CommunityEventAttendeeOutputDTO> update(Long id, CommunityEventAttendeeInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityEventAttendee", id)))
                    .flatMap(existing -> {
                        existing.setEventId(inputDTO.getEventId());
                        existing.setUserId(inputDTO.getUserId());
                        existing.setRsvpStatus(inputDTO.getRsvpStatus());
                        existing.setAttended(inputDTO.getAttended());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityEventAttendee", saved.getAttendeeId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CommunityEventAttendee
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityEventAttendee", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityEventAttendee", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_event_attendee", id))
            );
    }
    
    /**
     * Delete CommunityEventAttendee with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityEventAttendee", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityEventAttendee", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_event_attendee", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CommunityEventAttendeeOutputDTO toOutputDTO(CommunityEventAttendee entity) {
        return CommunityEventAttendeeOutputDTO.builder()
            .attendeeId(entity.getAttendeeId())
            .eventId(entity.getEventId())
            .userId(entity.getUserId())
            .rsvpStatus(entity.getRsvpStatus())
            .attended(entity.getAttended())
            .build();
    }
}