package com.example.service;

import com.example.entity.CommunityPropertyUserLink;
import com.example.dto.CommunityPropertyUserLinkInputDTO;
import com.example.dto.CommunityPropertyUserLinkOutputDTO;
import com.example.repository.CommunityPropertyUserLinkRepository;
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
 * Service class for CommunityPropertyUserLink business logic.
 */
@Service
@RequiredArgsConstructor
public class CommunityPropertyUserLinkService {
    
    private final CommunityPropertyUserLinkRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CommunityPropertyUserLink
     */
    @Transactional
    public Mono<CommunityPropertyUserLinkOutputDTO> create(CommunityPropertyUserLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CommunityPropertyUserLink entity = CommunityPropertyUserLink.builder()
                    .communityPropertyId(inputDTO.getCommunityPropertyId())
                    .userId(inputDTO.getUserId())
                    .comment(inputDTO.getComment())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("community_property_user_link")
                            .recordId(saved.getLinkId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityPropertyUserLink", saved.getLinkId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CommunityPropertyUserLink by ID
     */
    public Mono<CommunityPropertyUserLinkOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityPropertyUserLink", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CommunityPropertyUserLinks
     */
    public Flux<CommunityPropertyUserLinkOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CommunityPropertyUserLinks with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CommunityPropertyUserLinkOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CommunityPropertyUserLink> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "community_property_user_link", groupIds);
                            Flux<CommunityPropertyUserLink> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "community_property_user_link", groupIds, size, offset);
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
     * Update CommunityPropertyUserLink
     */
    @Transactional
    public Mono<CommunityPropertyUserLinkOutputDTO> update(Long id, CommunityPropertyUserLinkInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityPropertyUserLink", id)))
                    .flatMap(existing -> {
                        existing.setCommunityPropertyId(inputDTO.getCommunityPropertyId());
                        existing.setUserId(inputDTO.getUserId());
                        existing.setComment(inputDTO.getComment());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityPropertyUserLink", saved.getLinkId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CommunityPropertyUserLink
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityPropertyUserLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityPropertyUserLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_property_user_link", id))
            );
    }
    
    /**
     * Delete CommunityPropertyUserLink with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityPropertyUserLink", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityPropertyUserLink", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_property_user_link", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CommunityPropertyUserLinkOutputDTO toOutputDTO(CommunityPropertyUserLink entity) {
        return CommunityPropertyUserLinkOutputDTO.builder()
            .linkId(entity.getLinkId())
            .communityPropertyId(entity.getCommunityPropertyId())
            .userId(entity.getUserId())
            .comment(entity.getComment())
            .build();
    }
}