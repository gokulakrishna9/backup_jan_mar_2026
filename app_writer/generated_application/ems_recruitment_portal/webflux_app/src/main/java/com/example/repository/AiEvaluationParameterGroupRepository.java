package com.example.repository;

import com.example.entity.AiEvaluationParameterGroup;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import java.util.List;

/**
 * Repository interface for AiEvaluationParameterGroup entity.
 */
@Repository
public interface AiEvaluationParameterGroupRepository extends R2dbcRepository<AiEvaluationParameterGroup, Long> {

    @Query("SELECT * FROM ems_ai_evaluation_parameter_group ORDER BY aievaluationparametergroup_id LIMIT :size OFFSET :offset")
    Flux<AiEvaluationParameterGroup> findAllPaged(int size, long offset);

    @Query("SELECT COUNT(*) FROM ems_ai_evaluation_parameter_group")
    Mono<Long> countAll();

    @Query("SELECT DISTINCT t.* FROM ems_ai_evaluation_parameter_group t WHERE (SELECT is_super_user FROM auth_user WHERE auth_user_id=:authUserId) = true OR EXISTS (SELECT 1 FROM user_group_membership JOIN user_group ON user_group.group_id=user_group_membership.group_id WHERE user_group_membership.auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW()) AND user_group.is_super_group=true) OR EXISTS (SELECT 1 FROM document_group_table_scope JOIN document_group_membership ON document_group_membership.document_group_id=document_group_table_scope.document_group_id WHERE document_group_table_scope.table_name='ems_ai_evaluation_parameter_group' AND document_group_table_scope.allow_read=true AND (document_group_membership.expires_at IS NULL OR document_group_membership.expires_at > NOW()) AND (document_group_membership.auth_user_id=:authUserId OR document_group_membership.user_group_id IN (SELECT group_id FROM user_group_membership WHERE auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW())))) OR EXISTS (SELECT 1 FROM document_group_table_record_scope JOIN document_group_membership ON document_group_membership.document_group_id=document_group_table_record_scope.document_group_id WHERE document_group_table_record_scope.table_name='ems_ai_evaluation_parameter_group' AND document_group_table_record_scope.record_id = t.aievaluationparametergroup_id AND document_group_table_record_scope.allow_read=true AND (document_group_membership.expires_at IS NULL OR document_group_membership.expires_at > NOW()) AND (document_group_membership.auth_user_id=:authUserId OR document_group_membership.user_group_id IN (SELECT group_id FROM user_group_membership WHERE auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW())))) ORDER BY t.aievaluationparametergroup_id LIMIT :size OFFSET :offset")
    Flux<AiEvaluationParameterGroup> findAllPagedAuthorized(Long authUserId, int size, long offset);

    @Query("SELECT COUNT(DISTINCT t.aievaluationparametergroup_id) FROM ems_ai_evaluation_parameter_group t WHERE (SELECT is_super_user FROM auth_user WHERE auth_user_id=:authUserId) = true OR EXISTS (SELECT 1 FROM user_group_membership JOIN user_group ON user_group.group_id=user_group_membership.group_id WHERE user_group_membership.auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW()) AND user_group.is_super_group=true) OR EXISTS (SELECT 1 FROM document_group_table_scope JOIN document_group_membership ON document_group_membership.document_group_id=document_group_table_scope.document_group_id WHERE document_group_table_scope.table_name='ems_ai_evaluation_parameter_group' AND document_group_table_scope.allow_read=true AND (document_group_membership.expires_at IS NULL OR document_group_membership.expires_at > NOW()) AND (document_group_membership.auth_user_id=:authUserId OR document_group_membership.user_group_id IN (SELECT group_id FROM user_group_membership WHERE auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW())))) OR EXISTS (SELECT 1 FROM document_group_table_record_scope JOIN document_group_membership ON document_group_membership.document_group_id=document_group_table_record_scope.document_group_id WHERE document_group_table_record_scope.table_name='ems_ai_evaluation_parameter_group' AND document_group_table_record_scope.record_id = t.aievaluationparametergroup_id AND document_group_table_record_scope.allow_read=true AND (document_group_membership.expires_at IS NULL OR document_group_membership.expires_at > NOW()) AND (document_group_membership.auth_user_id=:authUserId OR document_group_membership.user_group_id IN (SELECT group_id FROM user_group_membership WHERE auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW()))))")
    Mono<Long> countAuthorized(Long authUserId);

    @Query("SELECT COUNT(DISTINCT e.aievaluationparametergroup_id) FROM ems_ai_evaluation_parameter_group e " +
           "LEFT JOIN record_owner ro ON ro.table_name = :tableName AND ro.record_id = e.aievaluationparametergroup_id " +
           "LEFT JOIN query_group_record qgr ON qgr.table_name = :tableName AND qgr.record_id = e.aievaluationparametergroup_id " +
           "WHERE ro.auth_user_id = :authUserId OR qgr.query_group_id IN (:groupIds)")
    Mono<Long> countOwnedOrShared(Long authUserId, String tableName, List<Long> groupIds);

    @Query("SELECT DISTINCT e.* FROM ems_ai_evaluation_parameter_group e " +
           "LEFT JOIN record_owner ro ON ro.table_name = :tableName AND ro.record_id = e.aievaluationparametergroup_id " +
           "LEFT JOIN query_group_record qgr ON qgr.table_name = :tableName AND qgr.record_id = e.aievaluationparametergroup_id " +
           "WHERE ro.auth_user_id = :authUserId OR qgr.query_group_id IN (:groupIds) " +
           "LIMIT :limit OFFSET :offset")
    Flux<AiEvaluationParameterGroup> findAllPagedOwnedOrShared(Long authUserId, String tableName, List<Long> groupIds, int limit, long offset);

}