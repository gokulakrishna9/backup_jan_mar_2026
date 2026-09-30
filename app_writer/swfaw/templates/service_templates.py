"""Service templates for code generation."""


class ServiceTemplates:
    """Templates for service class generation."""
    
    SERVICE_TEMPLATE = """package {{ packageName }};

import {{ entityPackage }}.{{ entityName }};
import {{ dtoPackage }}.{{ entityName }}InputDTO;
import {{ dtoPackage }}.{{ entityName }}OutputDTO;
import {{ repositoryPackage }}.{{ repositoryName }};
import {{ exceptionPackage }}.EntityNotFoundException;
import {{ dtoPackage }}.PageResponse;
{% if hasAuthorization %}import {{ repositoryPackage }}.RecordOwnerRepository;
import {{ repositoryPackage }}.QueryGroupRecordRepository;
import {{ repositoryPackage }}.QueryGroupMemberRepository;
import {{ repositoryPackage }}.AuthUserRepository;
import {{ entityPackage }}.RecordOwner;
import {{ securityPackage }}.SecurityContextHolder;
import {{ authPackage }}.JwtService;
{% endif %}{% if hasActivityTracking %}import {{ servicePackage }}.ActivityTrackingService;
import org.springframework.web.server.ServerWebExchange;
{% endif %}import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;
{% if hasAuthorization %}import java.util.List;
{% endif %}
/**
 * Service class for {{ entityName }} business logic.
 */
@Service
@RequiredArgsConstructor
public class {{ className }} {
    
    private final {{ repositoryName }} repository;
{% if hasAuthorization %}    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
{% endif %}{% if hasActivityTracking %}    private final ActivityTrackingService activityTrackingService;
{% endif %}    
    /**
     * Create new {{ entityName }}
     */
    @Transactional
    public Mono<{{ entityName }}OutputDTO> create({{ entityName }}InputDTO inputDTO{% if hasActivityTracking %}, ServerWebExchange exchange{% endif %}) {
{% if hasAuthorization %}        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
{% if singleRecordPerUser %}                // Single-record-per-user: reject if user already owns a record
                return repository.findByOwnerUserId(user.getAuthUserId())
                    .flatMap(existing -> Mono.<{{ entityName }}>error(
                        new IllegalStateException("{{ entityName }}: only one record per user is allowed")))
                    .switchIfEmpty(Mono.defer(() -> {
                        {{ entityName }} entity = {{ entityName }}.builder()
{% for field in fields %}                            .{{ field.fieldName }}(inputDTO.get{{ field.fieldNameCapitalized }}())
{% endfor %}{% if hasAuditFields %}                            .createdAt(LocalDateTime.now())
                            .updatedAt(LocalDateTime.now())
{% endif %}                            .build();
                        
                        return repository.save(entity)
                            .flatMap(saved -> {
                                RecordOwner recordOwner = RecordOwner.builder()
                                    .authUserId(user.getAuthUserId())
                                    .tableName("{{ tableName }}")
                                    .recordId(saved.get{{ idFieldCapitalized }}())
                                    .createdAt(LocalDateTime.now())
                                    .build();
                                return recordOwnerRepository.save(recordOwner)
                                    .thenReturn(saved);
                            });
                    }))
{% if hasActivityTracking %}                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "{{ entityName }}", saved.get{{ idFieldCapitalized }}(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
{% endif %}                    .map(this::toOutputDTO);
{% else %}                {{ entityName }} entity = {{ entityName }}.builder()
{% for field in fields %}                    .{{ field.fieldName }}(inputDTO.get{{ field.fieldNameCapitalized }}())
{% endfor %}{% if hasAuditFields %}                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
{% endif %}                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("{{ tableName }}")
                            .recordId(saved.get{{ idFieldCapitalized }}())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
{% if hasActivityTracking %}                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "{{ entityName }}", saved.get{{ idFieldCapitalized }}(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
{% endif %}                    .map(this::toOutputDTO);
{% endif %}            });
{% else %}        {{ entityName }} entity = {{ entityName }}.builder()
{% for field in fields %}            .{{ field.fieldName }}(inputDTO.get{{ field.fieldNameCapitalized }}())
{% endfor %}{% if hasAuditFields %}            .createdAt(LocalDateTime.now())
            .updatedAt(LocalDateTime.now())
{% endif %}            .build();
        
        return repository.save(entity)
            .map(this::toOutputDTO);
{% endif %}    }
    
    /**
     * Find {{ entityName }} by ID
     */
    public Mono<{{ entityName }}OutputDTO> findById(Long id) {
{% if hasSoftDelete %}        return repository.findByIdAndDeletedAtIsNull(id)
{% else %}        return repository.findById(id)
{% endif %}            .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all {{ entityName }}s
     */
    public Flux<{{ entityName }}OutputDTO> findAll() {
{% if hasSoftDelete %}        return repository.findAllByDeletedAtIsNull()
{% else %}        return repository.findAll()
{% endif %}            .map(this::toOutputDTO);
    }
    
    /**
     * Find {{ entityName }}s with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<{{ entityName }}OutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
{% if hasAuthorization %}        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
{% if hasSoftDelete %}                    Mono<Long> countMono = repository.countByDeletedAtIsNull();
                    Flux<{{ entityName }}> dataMono = repository.findAllPagedByDeletedAtIsNull(size, offset);
{% else %}                    Mono<Long> countMono = repository.countAll();
                    Flux<{{ entityName }}> dataMono = repository.findAllPaged(size, offset);
{% endif %}                    return countMono.flatMap(total ->
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
{% if hasSoftDelete %}                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "{{ tableName }}", groupIds);
                            Flux<{{ entityName }}> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "{{ tableName }}", groupIds, size, offset);
{% else %}                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "{{ tableName }}", groupIds);
                            Flux<{{ entityName }}> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "{{ tableName }}", groupIds, size, offset);
{% endif %}                            return countMono.flatMap(total ->
                                dataMono.map(this::toOutputDTO)
                                    .collectList()
                                    .map(content -> PageResponse.of(content, total, page, size))
                            );
                        });
                }
            });
{% else %}{% if hasSoftDelete %}        Mono<Long> countMono = repository.countByDeletedAtIsNull();
        Flux<{{ entityName }}> dataMono = repository.findAllPagedByDeletedAtIsNull(size, offset);
{% else %}        Mono<Long> countMono = repository.countAll();
        Flux<{{ entityName }}> dataMono = repository.findAllPaged(size, offset);
{% endif %}        return countMono.flatMap(total ->
            dataMono.map(this::toOutputDTO)
                .collectList()
                .map(content -> PageResponse.of(content, total, page, size))
        );
{% endif %}    }
    
    /**
     * Update {{ entityName }}
     */
    @Transactional
    public Mono<{{ entityName }}OutputDTO> update(Long id, {{ entityName }}InputDTO inputDTO{% if hasActivityTracking %}, ServerWebExchange exchange{% endif %}) {
{% if hasAuthorization %}        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
{% if hasSoftDelete %}                repository.findByIdAndDeletedAtIsNull(id)
{% else %}                repository.findById(id)
{% endif %}                    .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
                    .flatMap(existing -> {
{% for field in fields %}                        existing.set{{ field.fieldNameCapitalized }}(inputDTO.get{{ field.fieldNameCapitalized }}());
{% endfor %}{% if hasAuditFields %}                        existing.setUpdatedAt(LocalDateTime.now());
{% endif %}                        return repository.save(existing);
                    })
{% if hasActivityTracking %}                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "{{ entityName }}", saved.get{{ idFieldCapitalized }}(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
{% endif %}                    .map(this::toOutputDTO)
            );
{% else %}{% if hasSoftDelete %}        return repository.findByIdAndDeletedAtIsNull(id)
{% else %}        return repository.findById(id)
{% endif %}            .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
            .flatMap(existing -> {
{% for field in fields %}                existing.set{{ field.fieldNameCapitalized }}(inputDTO.get{{ field.fieldNameCapitalized }}());
{% endfor %}{% if hasAuditFields %}                existing.setUpdatedAt(LocalDateTime.now());
{% endif %}                return repository.save(existing);
            })
            .map(this::toOutputDTO);
{% endif %}    }
    
    /**
{% if hasSoftDelete %}     * Soft delete {{ entityName }}
{% else %}     * Delete {{ entityName }}
{% endif %}     */
    @Transactional
    public Mono<Void> delete(Long id{% if hasActivityTracking %}, ServerWebExchange exchange{% endif %}) {
{% if hasAuthorization %}        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
{% if hasSoftDelete %}                repository.findByIdAndDeletedAtIsNull(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
                    .flatMap(entity -> {
                        entity.setDeletedAt(LocalDateTime.now());
                        return repository.save(entity);
                    })
{% if hasActivityTracking %}                    .flatMap(saved -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "{{ entityName }}", id, saved,
                            activityTrackingService.getIpAddress(exchange), null)
                        .thenReturn(saved))
{% endif %}                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("{{ tableName }}", id))
                    .then()
{% else %}{% if hasActivityTracking %}                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "{{ entityName }}", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("{{ tableName }}", id))
                    .then()
{% else %}                repository.deleteById(id)
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("{{ tableName }}", id))
                    .then()
{% endif %}{% endif %}            );
{% else %}{% if hasSoftDelete %}        return repository.findByIdAndDeletedAtIsNull(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
            .flatMap(entity -> {
                entity.setDeletedAt(LocalDateTime.now());
                return repository.save(entity);
            })
            .then();
{% else %}        return repository.deleteById(id);
{% endif %}{% endif %}    }
    
    /**
{% if hasSoftDelete %}     * Soft delete {{ entityName }} with justification (for audit purposes)
{% else %}     * Delete {{ entityName }} with justification (for audit purposes)
{% endif %}     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification{% if hasActivityTracking %}, ServerWebExchange exchange{% endif %}) {
{% if hasAuthorization %}        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
{% if hasSoftDelete %}                repository.findByIdAndDeletedAtIsNull(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
                    .flatMap(entity -> {
                        entity.setDeletedAt(LocalDateTime.now());
                        return repository.save(entity);
                    })
{% if hasActivityTracking %}                    .flatMap(saved -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "{{ entityName }}", id, saved,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .thenReturn(saved))
{% endif %}                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("{{ tableName }}", id))
                    .then()
{% else %}{% if hasActivityTracking %}                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "{{ entityName }}", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("{{ tableName }}", id))
                    .then()
{% else %}                repository.deleteById(id)
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("{{ tableName }}", id))
                    .then()
{% endif %}{% endif %}            );
{% else %}{% if hasSoftDelete %}        return repository.findByIdAndDeletedAtIsNull(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("{{ entityName }}", id)))
            .flatMap(entity -> {
                entity.setDeletedAt(LocalDateTime.now());
                return repository.save(entity);
            })
            .then();
{% else %}        return repository.deleteById(id);
{% endif %}{% endif %}    }
    
{% if singleRecordPerUser and hasAuthorization %}    /**
     * Find the current user's own {{ entityName }} record (single-record-per-user).
     */
    public Mono<{{ entityName }}OutputDTO> findMyRecord() {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> repository.findByOwnerUserId(user.getAuthUserId()))
            .map(this::toOutputDTO);
    }
{% endif %}
    /**
     * Convert entity to output DTO
     */
    private {{ entityName }}OutputDTO toOutputDTO({{ entityName }} entity) {
        return {{ entityName }}OutputDTO.builder()
{% for field in outputFields %}            .{{ field.fieldName }}(entity.get{{ field.fieldNameCapitalized }}())
{% endfor %}{% if hasAuditFields %}            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
{% endif %}            .build();
    }
}
"""
