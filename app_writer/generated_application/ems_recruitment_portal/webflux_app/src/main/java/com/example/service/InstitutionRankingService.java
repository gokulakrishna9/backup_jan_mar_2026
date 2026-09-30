package com.example.service;

import com.example.entity.InstitutionRanking;
import com.example.dto.InstitutionRankingInputDTO;
import com.example.dto.InstitutionRankingOutputDTO;
import com.example.repository.InstitutionRankingRepository;
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
 * Service class for InstitutionRanking business logic.
 */
@Service
@RequiredArgsConstructor
public class InstitutionRankingService {
    
    private final InstitutionRankingRepository repository;
    private final RecordOwnerRepository recordOwnerRepository;
    private final QueryGroupRecordRepository queryGroupRecordRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Create new InstitutionRanking
     */
    @Transactional
    public Mono<InstitutionRankingOutputDTO> create(InstitutionRankingInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                InstitutionRanking entity = InstitutionRanking.builder()
                    .institutionId(inputDTO.getInstitutionId())
                    .rankingOrganization(inputDTO.getRankingOrganization())
                    .rankingYear(inputDTO.getRankingYear())
                    .overallRank(inputDTO.getOverallRank())
                    .countryRank(inputDTO.getCountryRank())
                    .category(inputDTO.getCategory())
                    .categoryRank(inputDTO.getCategoryRank())
                    .score(inputDTO.getScore())
                    .build();
                
                return repository.save(entity)
                    .flatMap(saved -> {
                        RecordOwner recordOwner = RecordOwner.builder()
                            .authUserId(user.getAuthUserId())
                            .tableName("institution_ranking")
                            .recordId(saved.getRankingId())
                            .createdAt(LocalDateTime.now())
                            .build();
                        return recordOwnerRepository.save(recordOwner)
                            .thenReturn(saved);
                    })
                    .flatMap(saved -> activityTrackingService.logCreate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionRanking", saved.getRankingId(),
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO);
            });
    }
    
    /**
     * Find InstitutionRanking by ID
     */
    public Mono<InstitutionRankingOutputDTO> findById(Long id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionRanking", id)))
            .map(this::toOutputDTO);
    }
    
    /**
     * Find all InstitutionRankings
     */
    public Flux<InstitutionRankingOutputDTO> findAll() {
        return repository.findAll()
            .map(this::toOutputDTO);
    }
    
    /**
     * Find InstitutionRankings with pagination (all filtering done in SQL)
     */
    public Mono<PageResponse<InstitutionRankingOutputDTO>> findAllPaged(int page, int size) {
        long offset = (long) page * size;
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> {
                List<String> roles = user.getRoles();
                boolean isAdmin = roles.contains("SUPER_ADMIN") || roles.contains("TABLE_ADMIN");
                
                if (isAdmin) {
                    Mono<Long> countMono = repository.countAll();
                    Flux<InstitutionRanking> dataMono = repository.findAllPaged(size, offset);
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
                            Mono<Long> countMono = repository.countOwnedOrShared(authUserId, "institution_ranking", groupIds);
                            Flux<InstitutionRanking> dataMono = repository.findAllPagedOwnedOrShared(authUserId, "institution_ranking", groupIds, size, offset);
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
     * Update InstitutionRanking
     */
    @Transactional
    public Mono<InstitutionRankingOutputDTO> update(Long id, InstitutionRankingInputDTO inputDTO, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionRanking", id)))
                    .flatMap(existing -> {
                        existing.setInstitutionId(inputDTO.getInstitutionId());
                        existing.setRankingOrganization(inputDTO.getRankingOrganization());
                        existing.setRankingYear(inputDTO.getRankingYear());
                        existing.setOverallRank(inputDTO.getOverallRank());
                        existing.setCountryRank(inputDTO.getCountryRank());
                        existing.setCategory(inputDTO.getCategory());
                        existing.setCategoryRank(inputDTO.getCategoryRank());
                        existing.setScore(inputDTO.getScore());
                        return repository.save(existing);
                    })
                    .flatMap(saved -> activityTrackingService.logUpdate(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionRanking", saved.getRankingId(),
                            null,
                            activityTrackingService.getIpAddress(exchange),
                            activityTrackingService.getUserAgent(exchange))
                        .thenReturn(saved))
                    .map(this::toOutputDTO)
            );
    }
    
    /**
     * Delete InstitutionRanking
     */
    @Transactional
    public Mono<Void> delete(Long id, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionRanking", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionRanking", id, entity,
                            activityTrackingService.getIpAddress(exchange), null)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_ranking", id))
            );
    }
    
    /**
     * Delete InstitutionRanking with justification (for audit purposes)
     */
    @Transactional
    public Mono<Void> deleteWithJustification(Long id, String justification, ServerWebExchange exchange) {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> 
                repository.findById(id)
                    .switchIfEmpty(Mono.error(new EntityNotFoundException("InstitutionRanking", id)))
                    .flatMap(entity -> activityTrackingService.logDelete(
                            user.getAuthUserId(), user.getUsername(),
                            "InstitutionRanking", id, entity,
                            activityTrackingService.getIpAddress(exchange), justification)
                        .then(repository.deleteById(id)))
                    .then(recordOwnerRepository.deleteByTableNameAndRecordId("institution_ranking", id))
            );
    }
    
    /**
     * Convert entity to output DTO
     */
    private InstitutionRankingOutputDTO toOutputDTO(InstitutionRanking entity) {
        return InstitutionRankingOutputDTO.builder()
            .rankingId(entity.getRankingId())
            .institutionId(entity.getInstitutionId())
            .rankingOrganization(entity.getRankingOrganization())
            .rankingYear(entity.getRankingYear())
            .overallRank(entity.getOverallRank())
            .countryRank(entity.getCountryRank())
            .category(entity.getCategory())
            .categoryRank(entity.getCategoryRank())
            .score(entity.getScore())
            .build();
    }
}