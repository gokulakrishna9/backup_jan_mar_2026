package com.example.service;

import com.example.entity.MarketTrendFile;
import com.example.dto.MarketTrendFileInputDTO;
import com.example.dto.MarketTrendFileOutputDTO;
import com.example.repository.MarketTrendFileRepository;
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
 * Service class for MarketTrendFile business logic.
 */
@Service
@RequiredArgsConstructor
public class MarketTrendFileService {
    
    private final MarketTrendFileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new MarketTrendFile
     */
    @Transactional
    public Mono<MarketTrendFileOutputDTO> create(MarketTrendFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                MarketTrendFile entity = MarketTrendFile.builder()
                    .trendId(inputDTO.getTrendId())
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
                    .source(inputDTO.getSource())
                    .reportDate(inputDTO.getReportDate())
                    .downloadCount(inputDTO.getDownloadCount())
                    .thumbnailLocation(inputDTO.getThumbnailLocation())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("market_trend_file")
                            .recordId(saved.getFileId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendFile", saved.getFileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find MarketTrendFile by ID
     */
    public Mono<MarketTrendFileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendFile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all MarketTrendFiles
     */
    public Flux<MarketTrendFileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find MarketTrendFiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<MarketTrendFileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<MarketTrendFile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "market_trend_file", groupIds);
                            Flux<MarketTrendFile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "market_trend_file", groupIds, size, offset);
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
     * Update MarketTrendFile
     */
    @Transactional
    public Mono<MarketTrendFileOutputDTO> update(Long id, MarketTrendFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendFile", id)))
                    .flatMap(existing -> {
                        existing.setTrendId(inputDTO.getTrendId());
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
                        existing.setSource(inputDTO.getSource());
                        existing.setReportDate(inputDTO.getReportDate());
                        existing.setDownloadCount(inputDTO.getDownloadCount());
                        existing.setThumbnailLocation(inputDTO.getThumbnailLocation());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendFile", saved.getFileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete MarketTrendFile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_file", id))
            );
    }
    
    /**
     * Delete MarketTrendFile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("MarketTrendFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "MarketTrendFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("market_trend_file", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private MarketTrendFileOutputDTO toOutputDTO(MarketTrendFile entity) {
        return MarketTrendFileOutputDTO.builder()
            .fileId(entity.getFileId())
            .trendId(entity.getTrendId())
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
            .source(entity.getSource())
            .reportDate(entity.getReportDate())
            .downloadCount(entity.getDownloadCount())
            .thumbnailLocation(entity.getThumbnailLocation())
            .build();
    }
}