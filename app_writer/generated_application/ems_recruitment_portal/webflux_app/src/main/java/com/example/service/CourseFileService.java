package com.example.service;

import com.example.entity.CourseFile;
import com.example.dto.CourseFileInputDTO;
import com.example.dto.CourseFileOutputDTO;
import com.example.repository.CourseFileRepository;
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
 * Service class for CourseFile business logic.
 */
@Service
@RequiredArgsConstructor
public class CourseFileService {
    
    private final CourseFileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new CourseFile
     */
    @Transactional
    public Mono<CourseFileOutputDTO> create(CourseFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                CourseFile entity = CourseFile.builder()
                    .courseId(inputDTO.getCourseId())
                    .moduleId(inputDTO.getModuleId())
                    .lessonId(inputDTO.getLessonId())
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
                    .isDownloadable(inputDTO.getIsDownloadable())
                    .requiresEnrollment(inputDTO.getRequiresEnrollment())
                    .downloadCount(inputDTO.getDownloadCount())
                    .thumbnailLocation(inputDTO.getThumbnailLocation())
                    .durationSeconds(inputDTO.getDurationSeconds())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("course_file")
                            .recordId(saved.getFileId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseFile", saved.getFileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find CourseFile by ID
     */
    public Mono<CourseFileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseFile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all CourseFiles
     */
    public Flux<CourseFileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find CourseFiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<CourseFileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<CourseFile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "course_file", groupIds);
                            Flux<CourseFile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "course_file", groupIds, size, offset);
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
     * Update CourseFile
     */
    @Transactional
    public Mono<CourseFileOutputDTO> update(Long id, CourseFileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseFile", id)))
                    .flatMap(existing -> {
                        existing.setCourseId(inputDTO.getCourseId());
                        existing.setModuleId(inputDTO.getModuleId());
                        existing.setLessonId(inputDTO.getLessonId());
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
                        existing.setIsDownloadable(inputDTO.getIsDownloadable());
                        existing.setRequiresEnrollment(inputDTO.getRequiresEnrollment());
                        existing.setDownloadCount(inputDTO.getDownloadCount());
                        existing.setThumbnailLocation(inputDTO.getThumbnailLocation());
                        existing.setDurationSeconds(inputDTO.getDurationSeconds());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseFile", saved.getFileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete CourseFile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_file", id))
            );
    }
    
    /**
     * Delete CourseFile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("CourseFile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "CourseFile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("course_file", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private CourseFileOutputDTO toOutputDTO(CourseFile entity) {
        return CourseFileOutputDTO.builder()
            .fileId(entity.getFileId())
            .courseId(entity.getCourseId())
            .moduleId(entity.getModuleId())
            .lessonId(entity.getLessonId())
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
            .isDownloadable(entity.getIsDownloadable())
            .requiresEnrollment(entity.getRequiresEnrollment())
            .downloadCount(entity.getDownloadCount())
            .thumbnailLocation(entity.getThumbnailLocation())
            .durationSeconds(entity.getDurationSeconds())
            .build();
    }
}