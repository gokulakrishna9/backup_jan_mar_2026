package com.example.service;

import com.example.entity.CourseCommunityLink;
import com.example.dto.CourseCommunityLinkInputDTO;
import com.example.dto.CourseCommunityLinkOutputDTO;
import com.example.repository.CourseCommunityLinkRepository;
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
 * Service class for CourseCommunityLink business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseCommunityLinkService {
    
    private final CourseCommunityLinkRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseCommunityLink
     */
    @Transactional
    public Mono<CourseCommunityLinkOutputDTO> create(CourseCommunityLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseCommunityLink entity = CourseCommunityLink.builder()
                    .courseId(inputDTO.getCourseId())
                    .communityId(inputDTO.getCommunityId())
                    .linkType(inputDTO.getLinkType())
                    .isActive(inputDTO.getIsActive())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_community_link")
                            .recordId(saved.getLinkId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseCommunityLink", saved.getLinkId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseCommunityLink by ID
     */
    public Mono<CourseCommunityLinkOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseCommunityLink", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseCommunityLinks
     */
    public Flux<CourseCommunityLinkOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseCommunityLinks with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseCommunityLinkOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseCommunityLink> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_community_link", groupIds);
                            Flux<CourseCommunityLink> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_community_link", groupIds, size, offset);
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
     * Update CourseCommunityLink
     */
    @Transactional
    public Mono<CourseCommunityLinkOutputDTO> update(Long id, CourseCommunityLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseCommunityLink", id)))
                    .flatMap(existing -> {
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setCommunityId(inputDTO.getCommunityId());
                        existing.setLinkType(inputDTO.getLinkType());
                        existing.setIsActive(inputDTO.getIsActive());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseCommunityLink", saved.getLinkId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseCommunityLink
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseCommunityLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseCommunityLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_community_link", id))
            );
    }
    
    /**
     * Delete CourseCommunityLink with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseCommunityLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseCommunityLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_community_link", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CourseCommunityLinkOutputDTO toOutputDTO(CourseCommunityLink entity) {
        return CourseCommunityLinkOutputDTO.builder()
            .linkId(entity.getLinkId())
            .courseId(entity.getCourseId())
            .communityId(entity.getCommunityId())
            .linkType(entity.getLinkType())
            .isActive(entity.getIsActive())
            .build();
    }
}