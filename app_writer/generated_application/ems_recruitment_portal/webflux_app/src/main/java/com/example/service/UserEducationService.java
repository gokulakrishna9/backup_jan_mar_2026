package com.example.service;

import com.example.entity.UserEducation;
import com.example.dto.UserEducationInputDTO;
import com.example.dto.UserEducationOutputDTO;
import com.example.repository.UserEducationRepository;
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
 * Service class for UserEducation business logic.
 */
@Service
@RequiredArgsConstructor
public class UserEducationService {
    
    private final UserEducationRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new UserEducation
     */
    @Transactional
    public Mono<UserEducationOutputDTO> create(UserEducationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                UserEducation entity = UserEducation.builder()
                    .userId(inputDTO.getUserId())
                    .institutionId(inputDTO.getInstitutionId())
                    .degreeType(inputDTO.getDegreeType())
                    .fieldOfStudy(inputDTO.getFieldOfStudy())
                    .specialization(inputDTO.getSpecialization())
                    .startDate(inputDTO.getStartDate())
                    .endDate(inputDTO.getEndDate())
                    .gradeGpa(inputDTO.getGradeGpa())
                    .isVerified(inputDTO.getIsVerified())
                    .certificateDocumentId(inputDTO.getCertificateDocumentId())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("user_education")
                            .recordId(saved.getEducationId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserEducation", saved.getEducationId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find UserEducation by ID
     */
    public Mono<UserEducationOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("UserEducation", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all UserEducations
     */
    public Flux<UserEducationOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find UserEducations with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<UserEducationOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<UserEducation> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "user_education", groupIds);
                            Flux<UserEducation> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "user_education", groupIds, size, offset);
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
     * Update UserEducation
     */
    @Transactional
    public Mono<UserEducationOutputDTO> update(Long id, UserEducationInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserEducation", id)))
                    .flatMap(existing -> {
                        existing.setUserId(inputDTO.getUserId());
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setDegreeType(inputDTO.getDegreeType());
                        existing.setFieldOfStudy(inputDTO.getFieldOfStudy());
                        existing.setSpecialization(inputDTO.getSpecialization());
                        existing.setStartDate(inputDTO.getStartDate());
                        existing.setEndDate(inputDTO.getEndDate());
                        existing.setGradeGpa(inputDTO.getGradeGpa());
                        existing.setIsVerified(inputDTO.getIsVerified());
                        existing.setCertificateDocumentId(inputDTO.getCertificateDocumentId());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "UserEducation", saved.getEducationId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete UserEducation
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserEducation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserEducation", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_education", id))
            );
    }
    
    /**
     * Delete UserEducation with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("UserEducation", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "UserEducation", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("user_education", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private UserEducationOutputDTO toOutputDTO(UserEducation entity) {
        return UserEducationOutputDTO.builder()
            .educationId(entity.getEducationId())
            .userId(entity.getUserId())
            .institutionId(entity.getInstitutionId())
            .degreeType(entity.getDegreeType())
            .fieldOfStudy(entity.getFieldOfStudy())
            .specialization(entity.getSpecialization())
            .startDate(entity.getStartDate())
            .endDate(entity.getEndDate())
            .gradeGpa(entity.getGradeGpa())
            .isVerified(entity.getIsVerified())
            .certificateDocumentId(entity.getCertificateDocumentId())
            .build();
    }
}