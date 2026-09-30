package com.example.service;

import com.example.entity.UserFile;
import com.example.dto.UserFileInputDTO;
import com.example.dto.UserFileOutputDTO;
import com.example.repository.UserFileRepository;
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
 * Service class for UserFile business logic.
 */
@Service
@RequiredArgsConstructor
public class UserFileService {
    
    private final UserFileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserFile
     */
    @Transactional
    public Mono<UserFileOutputDTO> create(UserFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserFile entity = UserFile.builder()
                    .userId(inputDTO.getUserId())
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
                    .isVerified(inputDTO.getIsVerified())
                    .downloadCount(inputDTO.getDownloadCount())
                    .thumbnailLocation(inputDTO.getThumbnailLocation())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_file")
                            .recordId(saved.getFileId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserFile", saved.getFileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserFile by ID
     */
    public Mono<UserFileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserFile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserFiles
     */
    public Flux<UserFileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserFiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserFileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserFile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_file", groupIds);
                            Flux<UserFile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_file", groupIds, size, offset);
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
     * Update UserFile
     */
    @Transactional
    public Mono<UserFileOutputDTO> update(Long id, UserFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserFile", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
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
                        existing.setIsVerified(inputDTO.getIsVerified());
                        existing.setDownloadCount(inputDTO.getDownloadCount());
                        existing.setThumbnailLocation(inputDTO.getThumbnailLocation());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserFile", saved.getFileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserFile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_file", id))
            );
    }
    
    /**
     * Delete UserFile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_file", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserFileOutputDTO toOutputDTO(UserFile entity) {
        return UserFileOutputDTO.builder()
            .fileId(entity.getFileId())
            .userId(entity.getUserId())
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
            .isVerified(entity.getIsVerified())
            .downloadCount(entity.getDownloadCount())
            .thumbnailLocation(entity.getThumbnailLocation())
            .build();
    }
}