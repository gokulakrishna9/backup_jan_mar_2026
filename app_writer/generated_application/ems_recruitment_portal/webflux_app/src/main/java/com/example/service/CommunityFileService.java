package com.example.service;

import com.example.entity.CommunityFile;
import com.example.dto.CommunityFileInputDTO;
import com.example.dto.CommunityFileOutputDTO;
import com.example.repository.CommunityFileRepository;
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
 * Service class for CommunityFile business logic.
 */
@Service
@RequiredArgsConstructor
public class CommunityFileService {
    
    private final CommunityFileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CommunityFile
     */
    @Transactional
    public Mono<CommunityFileOutputDTO> create(CommunityFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CommunityFile entity = CommunityFile.builder()
                    .communityId(inputDTO.getCommunityId())
                    .postId(inputDTO.getPostId())
                    .eventId(inputDTO.getEventId())
                    .fileName(inputDTO.getFileName())
                    .originalFileName(inputDTO.getOriginalFileName())
                    .fileType(inputDTO.getFileType())
                    .fileExtension(inputDTO.getFileExtension())
                    .fileLocation(inputDTO.getFileLocation())
                    .fileSizeBytes(inputDTO.getFileSizeBytes())
                    .mimeType(inputDTO.getMimeType())
                    .description(inputDTO.getDescription())
                    .comment(inputDTO.getComment())
                    .category(inputDTO.getCategory())
                    .uploadedByUserId(inputDTO.getUploadedByUserId())
                    .downloadCount(inputDTO.getDownloadCount())
                    .thumbnailLocation(inputDTO.getThumbnailLocation())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("community_file")
                            .recordId(saved.getFileId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityFile", saved.getFileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CommunityFile by ID
     */
    public Mono<CommunityFileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityFile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CommunityFiles
     */
    public Flux<CommunityFileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CommunityFiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CommunityFileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CommunityFile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "community_file", groupIds);
                            Flux<CommunityFile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "community_file", groupIds, size, offset);
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
     * Update CommunityFile
     */
    @Transactional
    public Mono<CommunityFileOutputDTO> update(Long id, CommunityFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityFile", id)))
                    .flatMap(existing -> {
                        existing.setCommunityId(inputDTO.getCommunityId());
                        existing.setPostId(inputDTO.getPostId());
                        existing.setEventId(inputDTO.getEventId());
                        existing.setFileName(inputDTO.getFileName());
                        existing.setOriginalFileName(inputDTO.getOriginalFileName());
                        existing.setFileType(inputDTO.getFileType());
                        existing.setFileExtension(inputDTO.getFileExtension());
                        existing.setFileLocation(inputDTO.getFileLocation());
                        existing.setFileSizeBytes(inputDTO.getFileSizeBytes());
                        existing.setMimeType(inputDTO.getMimeType());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setComment(inputDTO.getComment());
                        existing.setCategory(inputDTO.getCategory());
                        existing.setUploadedByUserId(inputDTO.getUploadedByUserId());
                        existing.setDownloadCount(inputDTO.getDownloadCount());
                        existing.setThumbnailLocation(inputDTO.getThumbnailLocation());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityFile", saved.getFileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CommunityFile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_file", id))
            );
    }
    
    /**
     * Delete CommunityFile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CommunityFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CommunityFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("community_file", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CommunityFileOutputDTO toOutputDTO(CommunityFile entity) {
        return CommunityFileOutputDTO.builder()
            .fileId(entity.getFileId())
            .communityId(entity.getCommunityId())
            .postId(entity.getPostId())
            .eventId(entity.getEventId())
            .fileName(entity.getFileName())
            .originalFileName(entity.getOriginalFileName())
            .fileType(entity.getFileType())
            .fileExtension(entity.getFileExtension())
            .fileLocation(entity.getFileLocation())
            .fileSizeBytes(entity.getFileSizeBytes())
            .mimeType(entity.getMimeType())
            .description(entity.getDescription())
            .comment(entity.getComment())
            .category(entity.getCategory())
            .uploadedByUserId(entity.getUploadedByUserId())
            .downloadCount(entity.getDownloadCount())
            .thumbnailLocation(entity.getThumbnailLocation())
            .build();
    }
}