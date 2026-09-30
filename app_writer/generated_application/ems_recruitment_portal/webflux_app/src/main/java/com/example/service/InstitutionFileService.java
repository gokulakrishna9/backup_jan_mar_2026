package com.example.service;

import com.example.entity.InstitutionFile;
import com.example.dto.InstitutionFileInputDTO;
import com.example.dto.InstitutionFileOutputDTO;
import com.example.repository.InstitutionFileRepository;
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
 * Service class for InstitutionFile business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionFileService {
    
    private final InstitutionFileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new InstitutionFile
     */
    @Transactional
    public Mono<InstitutionFileOutputDTO> create(InstitutionFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                InstitutionFile entity = InstitutionFile.builder()
                    .institutionId(inputDTO.getInstitutionId())
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
                            .tableName("institution_file")
                            .recordId(saved.getFileId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionFile", saved.getFileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find InstitutionFile by ID
     */
    public Mono<InstitutionFileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionFile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all InstitutionFiles
     */
    public Flux<InstitutionFileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find InstitutionFiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionFileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<InstitutionFile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution_file", groupIds);
                            Flux<InstitutionFile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution_file", groupIds, size, offset);
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
     * Update InstitutionFile
     */
    @Transactional
    public Mono<InstitutionFileOutputDTO> update(Long id, InstitutionFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionFile", id)))
                    .flatMap(existing -> {
                        existing.setInstitutionId(inputDTO.getInstitutionId());
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
                            "InstitutionFile", saved.getFileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete InstitutionFile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_file", id))
            );
    }
    
    /**
     * Delete InstitutionFile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_file", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionFileOutputDTO toOutputDTO(InstitutionFile entity) {
        return InstitutionFileOutputDTO.builder()
            .fileId(entity.getFileId())
            .institutionId(entity.getInstitutionId())
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