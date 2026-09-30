package com.example.service;

import com.example.entity.InstitutionDepartment;
import com.example.dto.InstitutionDepartmentInputDTO;
import com.example.dto.InstitutionDepartmentOutputDTO;
import com.example.repository.InstitutionDepartmentRepository;
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
 * Service class for InstitutionDepartment business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionDepartmentService {
    
    private final InstitutionDepartmentRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new InstitutionDepartment
     */
    @Transactional
    public Mono<InstitutionDepartmentOutputDTO> create(InstitutionDepartmentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                InstitutionDepartment entity = InstitutionDepartment.builder()
                    .institutionId(inputDTO.getInstitutionId())
                    .departmentName(inputDTO.getDepartmentName())
                    .description(inputDTO.getDescription())
                    .headOfDepartmentUserId(inputDTO.getHeadOfDepartmentUserId())
                    .contactEmail(inputDTO.getContactEmail())
                    .contactPhone(inputDTO.getContactPhone())
                    .isActive(inputDTO.getIsActive())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("institution_department")
                            .recordId(saved.getDepartmentId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionDepartment", saved.getDepartmentId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find InstitutionDepartment by ID
     */
    public Mono<InstitutionDepartmentOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionDepartment", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all InstitutionDepartments
     */
    public Flux<InstitutionDepartmentOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find InstitutionDepartments with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionDepartmentOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<InstitutionDepartment> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution_department", groupIds);
                            Flux<InstitutionDepartment> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution_department", groupIds, size, offset);
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
     * Update InstitutionDepartment
     */
    @Transactional
    public Mono<InstitutionDepartmentOutputDTO> update(Long id, InstitutionDepartmentInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionDepartment", id)))
                    .flatMap(existing -> {
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setDepartmentName(inputDTO.getDepartmentName());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setHeadOfDepartmentUserId(inputDTO.getHeadOfDepartmentUserId());
                        existing.setContactEmail(inputDTO.getContactEmail());
                        existing.setContactPhone(inputDTO.getContactPhone());
                        existing.setIsActive(inputDTO.getIsActive());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionDepartment", saved.getDepartmentId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete InstitutionDepartment
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionDepartment", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionDepartment", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_department", id))
            );
    }
    
    /**
     * Delete InstitutionDepartment with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionDepartment", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionDepartment", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_department", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionDepartmentOutputDTO toOutputDTO(InstitutionDepartment entity) {
        return InstitutionDepartmentOutputDTO.builder()
            .departmentId(entity.getDepartmentId())
            .institutionId(entity.getInstitutionId())
            .departmentName(entity.getDepartmentName())
            .description(entity.getDescription())
            .headOfDepartmentUserId(entity.getHeadOfDepartmentUserId())
            .contactEmail(entity.getContactEmail())
            .contactPhone(entity.getContactPhone())
            .isActive(entity.getIsActive())
            .build();
    }
}