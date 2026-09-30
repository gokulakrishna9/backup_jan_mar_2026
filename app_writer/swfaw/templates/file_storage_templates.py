"""File storage templates - templates for file storage components."""


class FileStorageTemplates:
    """Templates for file storage entities, repositories, services, and controllers."""

    @staticmethod
    def generate_storage_provider_interface(package_name: str) -> str:
        """Generate StorageProvider interface for abstracting file storage backends."""
        return f"""package {package_name}.storage;

import reactor.core.publisher.Mono;

/**
 * Interface for abstracting binary file storage operations.
 * Implementations can target local filesystem, S3/MinIO, or other backends.
 */
public interface StorageProvider {{

    /**
     * Store binary content at the given path.
     * @param path relative storage path
     * @param content file bytes
     * @return Mono completing when store finishes
     */
    Mono<Void> store(String path, byte[] content);

    /**
     * Retrieve binary content from the given path.
     * @param path relative storage path
     * @return Mono emitting file bytes
     */
    Mono<byte[]> retrieve(String path);

    /**
     * Delete the file at the given path.
     * @param path relative storage path
     * @return Mono completing when delete finishes
     */
    Mono<Void> delete(String path);

    /**
     * Check whether a file exists at the given path.
     * @param path relative storage path
     * @return Mono emitting true if file exists
     */
    Mono<Boolean> exists(String path);
}}
"""

    @staticmethod
    def generate_local_storage_provider(package_name: str, local_base_path: str) -> str:
        """Generate LocalStorageProvider that stores files on local filesystem."""
        return f"""package {package_name}.storage;

import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

/**
 * Local filesystem implementation of StorageProvider.
 * All I/O operations are wrapped in Mono.fromCallable() with Schedulers.boundedElastic()
 * to avoid blocking the reactive event loop.
 */
@Component
public class LocalStorageProvider implements StorageProvider {{

    private final Path basePath = Paths.get("{local_base_path}");

    @Override
    public Mono<Void> store(String path, byte[] content) {{
        return Mono.fromCallable(() -> {{
            Path filePath = basePath.resolve(path);
            Files.createDirectories(filePath.getParent());
            Files.write(filePath, content, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
            return (Void) null;
        }}).subscribeOn(Schedulers.boundedElastic()).then();
    }}

    @Override
    public Mono<byte[]> retrieve(String path) {{
        return Mono.fromCallable(() -> {{
            Path filePath = basePath.resolve(path);
            return Files.readAllBytes(filePath);
        }}).subscribeOn(Schedulers.boundedElastic());
    }}

    @Override
    public Mono<Void> delete(String path) {{
        return Mono.fromCallable(() -> {{
            Path filePath = basePath.resolve(path);
            Files.deleteIfExists(filePath);
            return (Void) null;
        }}).subscribeOn(Schedulers.boundedElastic()).then();
    }}

    @Override
    public Mono<Boolean> exists(String path) {{
        return Mono.fromCallable(() -> {{
            Path filePath = basePath.resolve(path);
            return Files.exists(filePath);
        }}).subscribeOn(Schedulers.boundedElastic());
    }}
}}
"""

    @staticmethod
    def generate_s3_storage_provider(package_name: str) -> str:
        """Generate S3StorageProvider stub with all methods returning UnsupportedOperationException."""
        return f"""package {package_name}.storage;

import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * Amazon S3 / MinIO stub implementation of StorageProvider.
 * All methods return Mono.error(UnsupportedOperationException) until implemented.
 */
@Component
public class S3StorageProvider implements StorageProvider {{

    @Override
    public Mono<Void> store(String path, byte[] content) {{
        return Mono.error(new UnsupportedOperationException("S3 storage not yet implemented"));
    }}

    @Override
    public Mono<byte[]> retrieve(String path) {{
        return Mono.error(new UnsupportedOperationException("S3 storage not yet implemented"));
    }}

    @Override
    public Mono<Void> delete(String path) {{
        return Mono.error(new UnsupportedOperationException("S3 storage not yet implemented"));
    }}

    @Override
    public Mono<Boolean> exists(String path) {{
        return Mono.error(new UnsupportedOperationException("S3 storage not yet implemented"));
    }}
}}
"""

    @staticmethod
    def generate_file_metadata_entity(package_name: str) -> str:
        """Generate FileMetadata entity mapped to file_metadata table."""
        return f"""package {package_name}.storage;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity representing file metadata stored in the file_metadata table.
 * Tracks uploaded files with optional entity attachment references.
 */
@Table("file_metadata")
public class FileMetadata {{

    @Id
    private Long id;

    @Column("file_name")
    private String fileName;

    @Column("content_type")
    private String contentType;

    @Column("file_size")
    private Long fileSize;

    @Column("storage_path")
    private String storagePath;

    @Column("uploaded_at")
    private LocalDateTime uploadedAt;

    @Column("entity_type")
    private String entityType;

    @Column("entity_id")
    private Long entityId;

    @Column("uploaded_by_user_id")
    private Long uploadedByUserId;

    // Constructors
    public FileMetadata() {{
        this.uploadedAt = LocalDateTime.now();
    }}

    // Getters and Setters
    public Long getId() {{
        return id;
    }}

    public void setId(Long id) {{
        this.id = id;
    }}

    public String getFileName() {{
        return fileName;
    }}

    public void setFileName(String fileName) {{
        this.fileName = fileName;
    }}

    public String getContentType() {{
        return contentType;
    }}

    public void setContentType(String contentType) {{
        this.contentType = contentType;
    }}

    public Long getFileSize() {{
        return fileSize;
    }}

    public void setFileSize(Long fileSize) {{
        this.fileSize = fileSize;
    }}

    public String getStoragePath() {{
        return storagePath;
    }}

    public void setStoragePath(String storagePath) {{
        this.storagePath = storagePath;
    }}

    public LocalDateTime getUploadedAt() {{
        return uploadedAt;
    }}

    public void setUploadedAt(LocalDateTime uploadedAt) {{
        this.uploadedAt = uploadedAt;
    }}

    public String getEntityType() {{
        return entityType;
    }}

    public void setEntityType(String entityType) {{
        this.entityType = entityType;
    }}

    public Long getEntityId() {{
        return entityId;
    }}

    public void setEntityId(Long entityId) {{
        this.entityId = entityId;
    }}

    public Long getUploadedByUserId() {{
        return uploadedByUserId;
    }}

    public void setUploadedByUserId(Long uploadedByUserId) {{
        this.uploadedByUserId = uploadedByUserId;
    }}
}}
"""

    @staticmethod
    def generate_file_metadata_repository(package_name: str) -> str:
        """Generate FileMetadataRepository with custom query methods."""
        return f"""package {package_name}.storage;

import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for FileMetadata entity.
 * Provides reactive CRUD and custom query methods for file metadata.
 */
@Repository
public interface FileMetadataRepository extends ReactiveCrudRepository<FileMetadata, Long> {{

    Flux<FileMetadata> findByEntityTypeAndEntityId(String entityType, Long entityId);

    Mono<FileMetadata> findByStoragePath(String storagePath);
}}
"""

    @staticmethod
    def generate_file_storage_service(package_name: str, max_file_size_mb: int, allowed_content_types: list) -> str:
        """Generate FileStorageService with validation, auth checks, and reactive file operations."""
        # Build content type check code
        if allowed_content_types:
            content_types_java = ", ".join(f'"{ct}"' for ct in allowed_content_types)
            content_type_validation = f"""
        // Validate content type against allowed list
        java.util.List<String> allowedTypes = java.util.Arrays.asList({content_types_java});
        if (!allowedTypes.contains(contentType)) {{
            return Mono.error(new org.springframework.web.server.ResponseStatusException(
                org.springframework.http.HttpStatus.BAD_REQUEST,
                "Content type '" + contentType + "' is not allowed. Allowed types: " + allowedTypes));
        }}"""
        else:
            content_type_validation = ""

        max_bytes = max_file_size_mb * 1024 * 1024

        return f"""package {package_name}.storage;

import {package_name}.security.SecurityContextHolder;
import org.springframework.http.codec.multipart.FilePart;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Service for managing file uploads, downloads, deletions, and listings.
 * Validates file size (max {max_file_size_mb} MB) and content types.
 * Enforces row-level authorization for entity-attached and standalone files.
 */
@Service
public class FileStorageService {{

    private static final long MAX_FILE_SIZE_BYTES = {max_bytes}L; // {max_file_size_mb} MB

    private final StorageProvider storageProvider;
    private final FileMetadataRepository fileMetadataRepository;
    private final SecurityContextHolder securityContextHolder;

    public FileStorageService(StorageProvider storageProvider,
                              FileMetadataRepository fileMetadataRepository,
                              SecurityContextHolder securityContextHolder) {{
        this.storageProvider = storageProvider;
        this.fileMetadataRepository = fileMetadataRepository;
        this.securityContextHolder = securityContextHolder;
    }}

    /**
     * Upload a file, optionally attaching it to an entity.
     * Validates file size and content type before storing.
     * For entity-attached files, checks CREATE permission on the entity.
     * For standalone files, records the uploader's user ID as owner.
     * Response includes inlineUrl for rich text editor embedding.
     */
    public Mono<FileMetadata> upload(FilePart filePart, String entityType, Long entityId) {{
        return securityContextHolder.getCurrentUser()
            .flatMap(user -> {{
                String contentType = filePart.headers().getContentType() != null
                    ? filePart.headers().getContentType().toString()
                    : "application/octet-stream";

                return filePart.content()
                    .reduce(new byte[0], (acc, dataBuffer) -> {{
                        byte[] bytes = new byte[dataBuffer.readableByteCount()];
                        dataBuffer.read(bytes);
                        byte[] combined = new byte[acc.length + bytes.length];
                        System.arraycopy(acc, 0, combined, 0, acc.length);
                        System.arraycopy(bytes, 0, combined, acc.length, bytes.length);
                        return combined;
                    }})
                    .flatMap(fileBytes -> {{
                        long fileSize = fileBytes.length;

                        // Validate file size
                        if (fileSize > MAX_FILE_SIZE_BYTES) {{
                            return Mono.error(new ResponseStatusException(HttpStatus.BAD_REQUEST,
                                "File size " + fileSize + " bytes exceeds maximum allowed size of " + MAX_FILE_SIZE_BYTES + " bytes ({max_file_size_mb} MB)"));
                        }}
{content_type_validation}

                        // Authorization check
                        Mono<Void> authCheck;
                        if (entityType != null && entityId != null) {{
                            // Entity-attached file: check CREATE permission on the entity
                            authCheck = securityContextHolder.checkPermission(user, entityType, entityId, "CREATE")
                                .flatMap(allowed -> {{
                                    if (!allowed) {{
                                        return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                                            "Access denied: CREATE permission required on " + entityType + " #" + entityId));
                                    }}
                                    return Mono.empty();
                                }});
                        }} else {{
                            // Standalone file: no entity auth needed at upload time
                            authCheck = Mono.empty();
                        }}

                        return authCheck.then(Mono.defer(() -> {{
                            String storagePath = UUID.randomUUID().toString() + "/" + filePart.filename();

                            return storageProvider.store(storagePath, fileBytes)
                                .then(Mono.defer(() -> {{
                                    FileMetadata metadata = new FileMetadata();
                                    metadata.setFileName(filePart.filename());
                                    metadata.setContentType(contentType);
                                    metadata.setFileSize(fileSize);
                                    metadata.setStoragePath(storagePath);
                                    metadata.setUploadedAt(LocalDateTime.now());
                                    metadata.setEntityType(entityType);
                                    metadata.setEntityId(entityId);
                                    metadata.setUploadedByUserId(user.getId());

                                    return fileMetadataRepository.save(metadata);
                                }}));
                        }}));
                    }});
            }});
    }}

    /**
     * Download a file by its metadata ID.
     * For entity-attached files, checks READ permission on the entity.
     * For standalone files, checks that the user is the owner or SUPER_ADMIN.
     */
    public Mono<byte[]> download(Long fileId) {{
        return securityContextHolder.getCurrentUser()
            .flatMap(user -> fileMetadataRepository.findById(fileId)
                .switchIfEmpty(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND, "File not found: " + fileId)))
                .flatMap(metadata -> {{
                    Mono<Void> authCheck;
                    if (metadata.getEntityType() != null && metadata.getEntityId() != null) {{
                        // Entity-attached: check READ permission
                        authCheck = securityContextHolder.checkPermission(user, metadata.getEntityType(), metadata.getEntityId(), "READ")
                            .flatMap(allowed -> {{
                                if (!allowed) {{
                                    return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                                        "Access denied: READ permission required on " + metadata.getEntityType() + " #" + metadata.getEntityId()));
                                }}
                                return Mono.empty();
                            }});
                    }} else {{
                        // Standalone: owner or SUPER_ADMIN
                        if (!user.getId().equals(metadata.getUploadedByUserId()) && !user.hasRole("SUPER_ADMIN")) {{
                            return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                                "Access denied: only the file owner or SUPER_ADMIN can access this file"));
                        }}
                        authCheck = Mono.empty();
                    }}
                    return authCheck.then(storageProvider.retrieve(metadata.getStoragePath()));
                }}));
    }}

    /**
     * Get file metadata by ID (used by controller for content disposition headers).
     */
    public Mono<FileMetadata> getMetadata(Long fileId) {{
        return fileMetadataRepository.findById(fileId)
            .switchIfEmpty(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND, "File not found: " + fileId)));
    }}

    /**
     * Delete a file by its metadata ID.
     * For entity-attached files, checks DELETE permission on the entity.
     * For standalone files, checks that the user is the owner or SUPER_ADMIN.
     */
    public Mono<Void> delete(Long fileId) {{
        return securityContextHolder.getCurrentUser()
            .flatMap(user -> fileMetadataRepository.findById(fileId)
                .switchIfEmpty(Mono.error(new ResponseStatusException(HttpStatus.NOT_FOUND, "File not found: " + fileId)))
                .flatMap(metadata -> {{
                    Mono<Void> authCheck;
                    if (metadata.getEntityType() != null && metadata.getEntityId() != null) {{
                        authCheck = securityContextHolder.checkPermission(user, metadata.getEntityType(), metadata.getEntityId(), "DELETE")
                            .flatMap(allowed -> {{
                                if (!allowed) {{
                                    return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                                        "Access denied: DELETE permission required on " + metadata.getEntityType() + " #" + metadata.getEntityId()));
                                }}
                                return Mono.empty();
                            }});
                    }} else {{
                        if (!user.getId().equals(metadata.getUploadedByUserId()) && !user.hasRole("SUPER_ADMIN")) {{
                            return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                                "Access denied: only the file owner or SUPER_ADMIN can delete this file"));
                        }}
                        authCheck = Mono.empty();
                    }}
                    return authCheck
                        .then(storageProvider.delete(metadata.getStoragePath()))
                        .then(fileMetadataRepository.delete(metadata));
                }}));
    }}

    /**
     * List all files attached to a specific entity.
     * Filters results to files the authenticated user has READ permission on.
     */
    public Flux<FileMetadata> listByEntity(String entityType, Long entityId) {{
        return securityContextHolder.getCurrentUser()
            .flatMapMany(user -> securityContextHolder.checkPermission(user, entityType, entityId, "READ")
                .flatMapMany(allowed -> {{
                    if (!allowed) {{
                        return Flux.error(new ResponseStatusException(HttpStatus.FORBIDDEN,
                            "Access denied: READ permission required on " + entityType + " #" + entityId));
                    }}
                    return fileMetadataRepository.findByEntityTypeAndEntityId(entityType, entityId);
                }}));
    }}

    /**
     * Delete all files attached to a specific entity.
     * Used when the parent entity is deleted.
     */
    public Mono<Void> deleteByEntity(String entityType, Long entityId) {{
        return fileMetadataRepository.findByEntityTypeAndEntityId(entityType, entityId)
            .flatMap(metadata -> storageProvider.delete(metadata.getStoragePath())
                .then(fileMetadataRepository.delete(metadata)))
            .then();
    }}
}}
"""

    @staticmethod
    def generate_file_controller(package_name: str) -> str:
        """Generate FileController with upload, download, inline, thumbnail, delete, and list-by-entity endpoints."""
        return f"""package {package_name}.storage;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.codec.multipart.FilePart;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * REST controller for file storage operations.
 * Provides upload, download (attachment), inline serving, thumbnail, delete,
 * and list-by-entity endpoints.
 */
@RestController
@RequestMapping("/api/files")
public class FileController {{

    private final FileStorageService fileStorageService;

    public FileController(FileStorageService fileStorageService) {{
        this.fileStorageService = fileStorageService;
    }}

    /**
     * Upload a file, optionally attaching it to an entity.
     * Response includes inlineUrl field for rich text editor embedding.
     * POST /api/files/upload
     */
    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Mono<java.util.Map<String, Object>> upload(
            @RequestPart("file") FilePart filePart,
            @RequestParam(value = "entityType", required = false) String entityType,
            @RequestParam(value = "entityId", required = false) Long entityId) {{
        return fileStorageService.upload(filePart, entityType, entityId)
            .map(metadata -> {{
                java.util.Map<String, Object> response = new java.util.LinkedHashMap<>();
                response.put("id", metadata.getId());
                response.put("fileName", metadata.getFileName());
                response.put("contentType", metadata.getContentType());
                response.put("fileSize", metadata.getFileSize());
                response.put("storagePath", metadata.getStoragePath());
                response.put("uploadedAt", metadata.getUploadedAt().toString());
                response.put("entityType", metadata.getEntityType());
                response.put("entityId", metadata.getEntityId());
                response.put("uploadedByUserId", metadata.getUploadedByUserId());
                response.put("inlineUrl", "/api/files/" + metadata.getId() + "/inline");
                return response;
            }});
    }}

    /**
     * Download a file as an attachment (triggers browser download).
     * GET /api/files/{{id}}/download
     * Returns Content-Disposition: attachment; filename="<originalFileName>"
     */
    @GetMapping("/{{id}}/download")
    public Mono<ResponseEntity<byte[]>> download(@PathVariable Long id) {{
        return fileStorageService.getMetadata(id)
            .flatMap(metadata -> fileStorageService.download(id)
                .map(bytes -> ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\\"" + metadata.getFileName() + "\\"")
                    .header(HttpHeaders.CONTENT_TYPE, metadata.getContentType())
                    .header(HttpHeaders.CONTENT_LENGTH, String.valueOf(bytes.length))
                    .body(bytes)));
    }}

    /**
     * Serve a file inline (for embedding in rich text editors, browser rendering).
     * GET /api/files/{{id}}/inline
     * Returns Content-Disposition: inline; filename="<originalFileName>"
     * Sets Cache-Control: max-age=3600, public
     */
    @GetMapping("/{{id}}/inline")
    public Mono<ResponseEntity<byte[]>> inline(@PathVariable Long id) {{
        return fileStorageService.getMetadata(id)
            .flatMap(metadata -> fileStorageService.download(id)
                .map(bytes -> ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\\"" + metadata.getFileName() + "\\"")
                    .header(HttpHeaders.CONTENT_TYPE, metadata.getContentType())
                    .header(HttpHeaders.CONTENT_LENGTH, String.valueOf(bytes.length))
                    .header(HttpHeaders.CACHE_CONTROL, "max-age=3600, public")
                    .body(bytes)));
    }}

    /**
     * Serve a thumbnail of an image file.
     * GET /api/files/{{id}}/thumbnail?width=N&height=N
     * Returns the original file if resizing is not supported or file is not an image.
     * Sets Cache-Control: max-age=3600, public
     */
    @GetMapping("/{{id}}/thumbnail")
    public Mono<ResponseEntity<byte[]>> thumbnail(
            @PathVariable Long id,
            @RequestParam(value = "width", defaultValue = "200") int width,
            @RequestParam(value = "height", defaultValue = "200") int height) {{
        return fileStorageService.getMetadata(id)
            .flatMap(metadata -> fileStorageService.download(id)
                .map(bytes -> {{
                    // TODO: Implement image resizing for JPEG, PNG, GIF, WebP
                    // For now, return the original file
                    return ResponseEntity.ok()
                        .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\\"" + metadata.getFileName() + "\\"")
                        .header(HttpHeaders.CONTENT_TYPE, metadata.getContentType())
                        .header(HttpHeaders.CONTENT_LENGTH, String.valueOf(bytes.length))
                        .header(HttpHeaders.CACHE_CONTROL, "max-age=3600, public")
                        .body(bytes);
                }}));
    }}

    /**
     * Delete a file by ID.
     * DELETE /api/files/{{id}}
     */
    @DeleteMapping("/{{id}}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(@PathVariable Long id) {{
        return fileStorageService.delete(id);
    }}

    /**
     * List all files attached to a specific entity.
     * GET /api/files/entity/{{entityType}}/{{entityId}}
     */
    @GetMapping("/entity/{{entityType}}/{{entityId}}")
    public Flux<FileMetadata> listByEntity(
            @PathVariable String entityType,
            @PathVariable Long entityId) {{
        return fileStorageService.listByEntity(entityType, entityId);
    }}
}}
"""
