package com.jobportal.service;

import com.jobportal.entity.EmployerProfile;
import com.jobportal.dto.EmployerProfileInputDTO;
import com.jobportal.dto.EmployerProfileOutputDTO;
import com.jobportal.repository.EmployerProfileRepository;
import com.jobportal.exception.EntityNotFoundException;
import com.jobportal.dto.PageResponse;
import com.jobportal.repository.RecordOwnerRepository;
import com.jobportal.repository.QueryGroupRecordRepository;
import com.jobportal.repository.QueryGroupMemberRepository;
import com.jobportal.repository.AuthUserRepository;
import com.jobportal.entity.RecordOwner;
import com.jobportal.security.SecurityContextHolder;
import com.jobportal.auth.JwtService;
import com.jobportal.service.ActivityTrackingService;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Service class for EmployerProfile business logic.
 */
@Service
@RequiredArgsConstructor
public class EmployerProfileService {
    
    private final EmployerProfileRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final AuthUserRepository authUserRepository;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new EmployerProfile
     */
    @Transactional
    public Mono<EmployerProfileOutputDTO> create(EmployerProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                // Single-record-per-user: reject if user already owns a record
                return repository.findByOwnerUserId(user.getAuthUserId())
                    .flatMap(existing -> Mono.<EmployerProfile>error(
                        new IllegalStateException("EmployerProfile: only one record per user is allowed")))
                    .switchIfEmpty(Mono.defer(() -> {
                        EmployerProfile entity = EmployerProfile.builder()
                            .companyname(inputDTO.getCompanyname())
                            .industry(inputDTO.getIndustry())
                            .website(inputDTO.getWebsite())
                            .logourl(inputDTO.getLogourl())
                            .description(inputDTO.getDescription())
                            .contactemail(inputDTO.getContactemail())
                            .createdAt(LocalDateTime.now())
                            .updatedAt(LocalDateTime.now())
                            .build();
                        
                        return repository.save(entity)
                            .flatMap(saved -> {
                                RecordOwner recordOwner = RecordOwner.builder()
                                    .authUserId(user.getAuthUserId())
                                    .tableName("employer_profile")
                                    .recordId(saved.getEmployerProfileId())
                                    .createdAt(LocalDateTime.now())
                                    .build();
                                return recordOwnerRepository.save(recordOwner)
                                    .thenReturn(saved);
                            });
                    }))
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "EmployerProfile", saved.getEmployerProfileId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find EmployerProfile by ID
     */
    public Mono<EmployerProfileOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("EmployerProfile", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all EmployerProfiles
     */
    public Flux<EmployerProfileOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find EmployerProfiles with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<EmployerProfileOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<EmployerProfile> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "employer_profile", groupIds);
                            Flux<EmployerProfile> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "employer_profile", groupIds, size, offset);
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
     * Update EmployerProfile
     */
    @Transactional
    public Mono<EmployerProfileOutputDTO> update(Long id, EmployerProfileInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("EmployerProfile", id)))
                    .flatMap(existing -> {
                        existing.setCompanyname(inputDTO.getCompanyname());
                        existing.setIndustry(inputDTO.getIndustry());
                        existing.setWebsite(inputDTO.getWebsite());
                        existing.setLogourl(inputDTO.getLogourl());
                        existing.setDescription(inputDTO.getDescription());
                        existing.setContactemail(inputDTO.getContactemail());
                        existing.setUpdatedAt(LocalDateTime.now());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "EmployerProfile", saved.getEmployerProfileId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete EmployerProfile
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("EmployerProfile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "EmployerProfile", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("employer_profile", id))
                    .then()
            );
    }
    
    /**
     * Delete EmployerProfile with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("EmployerProfile", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "EmployerProfile", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("employer_profile", id))
                    .then()
            );
    }
    
    /**
     * Find the current user's own EmployerProfile record (single-record-per-user).
     */
    public Mono<EmployerProfileOutputDTO> findMyRecord() {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> repository.findByOwnerUserId(user.getAuthUserId()))
            .map(this::toOutputDTO);
    }

    /**
     * Convert entity to output DTO
     */
    private EmployerProfileOutputDTO toOutputDTO(EmployerProfile entity) {
        return EmployerProfileOutputDTO.builder()
            .employerProfileId(entity.getEmployerProfileId())
            .companyname(entity.getCompanyname())
            .industry(entity.getIndustry())
            .website(entity.getWebsite())
            .logourl(entity.getLogourl())
            .description(entity.getDescription())
            .contactemail(entity.getContactemail())
            .createdAt(entity.getCreatedAt())
            .updatedAt(entity.getUpdatedAt())
            .build();
    }
}