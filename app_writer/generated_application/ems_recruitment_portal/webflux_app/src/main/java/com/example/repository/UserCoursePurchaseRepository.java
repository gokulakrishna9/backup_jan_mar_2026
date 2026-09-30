package com.example.repository;

import com.example.entity.UserCoursePurchase;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import java.util.List;

/**
 * Repository interface for UserCoursePurchase entity.
 */
@Repository
public interface UserCoursePurchaseRepository extends R2dbcRepository<UserCoursePurchase, Long> {

    @Query("SELECT * FROM ems_user_course_purchase ORDER BY usercoursepurchase_id LIMIT :size OFFSET :offset")
    Flux<UserCoursePurchase> findAllPaged(int size, long offset);

    @Query("SELECT COUNT(*) FROM ems_user_course_purchase")
    Mono<Long> countAll();

    @Query("SELECT DISTINCT t.* FROM ems_user_course_purchase t WHERE (SELECT is_super_user FROM auth_user WHERE auth_user_id=:authUserId) = true OR EXISTS (SELECT 1 FROM user_group_membership JOIN user_group ON user_group.group_id=user_group_membership.group_id WHERE user_group_membership.auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW()) AND user_group.is_super_group=true) OR EXISTS (SELECT 1 FROM document_group_table_scope JOIN document_group_membership ON document_group_membership.document_group_id=document_group_table_scope.document_group_id WHERE document_group_table_scope.table_name='ems_user_course_purchase' AND document_group_table_scope.allow_read=true AND (document_group_membership.expires_at IS NULL OR document_group_membership.expires_at > NOW()) AND (document_group_membership.auth_user_id=:authUserId OR document_group_membership.user_group_id IN (SELECT group_id FROM user_group_membership WHERE auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW())))) OR EXISTS (SELECT 1 FROM document_group_table_record_scope JOIN document_group_membership ON document_group_membership.document_group_id=document_group_table_record_scope.document_group_id WHERE document_group_table_record_scope.table_name='ems_user_course_purchase' AND document_group_table_record_scope.record_id = t.usercoursepurchase_id AND document_group_table_record_scope.allow_read=true AND (document_group_membership.expires_at IS NULL OR document_group_membership.expires_at > NOW()) AND (document_group_membership.auth_user_id=:authUserId OR document_group_membership.user_group_id IN (SELECT group_id FROM user_group_membership WHERE auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW())))) ORDER BY t.usercoursepurchase_id LIMIT :size OFFSET :offset")
    Flux<UserCoursePurchase> findAllPagedAuthorized(Long authUserId, int size, long offset);

    @Query("SELECT COUNT(DISTINCT t.usercoursepurchase_id) FROM ems_user_course_purchase t WHERE (SELECT is_super_user FROM auth_user WHERE auth_user_id=:authUserId) = true OR EXISTS (SELECT 1 FROM user_group_membership JOIN user_group ON user_group.group_id=user_group_membership.group_id WHERE user_group_membership.auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW()) AND user_group.is_super_group=true) OR EXISTS (SELECT 1 FROM document_group_table_scope JOIN document_group_membership ON document_group_membership.document_group_id=document_group_table_scope.document_group_id WHERE document_group_table_scope.table_name='ems_user_course_purchase' AND document_group_table_scope.allow_read=true AND (document_group_membership.expires_at IS NULL OR document_group_membership.expires_at > NOW()) AND (document_group_membership.auth_user_id=:authUserId OR document_group_membership.user_group_id IN (SELECT group_id FROM user_group_membership WHERE auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW())))) OR EXISTS (SELECT 1 FROM document_group_table_record_scope JOIN document_group_membership ON document_group_membership.document_group_id=document_group_table_record_scope.document_group_id WHERE document_group_table_record_scope.table_name='ems_user_course_purchase' AND document_group_table_record_scope.record_id = t.usercoursepurchase_id AND document_group_table_record_scope.allow_read=true AND (document_group_membership.expires_at IS NULL OR document_group_membership.expires_at > NOW()) AND (document_group_membership.auth_user_id=:authUserId OR document_group_membership.user_group_id IN (SELECT group_id FROM user_group_membership WHERE auth_user_id=:authUserId AND (user_group_membership.expires_at IS NULL OR user_group_membership.expires_at > NOW()))))")
    Mono<Long> countAuthorized(Long authUserId);

    @Query("SELECT COUNT(DISTINCT e.usercoursepurchase_id) FROM ems_user_course_purchase e " +
           "LEFT JOIN record_owner ro ON ro.table_name = :tableName AND ro.record_id = e.usercoursepurchase_id " +
           "LEFT JOIN query_group_record qgr ON qgr.table_name = :tableName AND qgr.record_id = e.usercoursepurchase_id " +
           "WHERE ro.auth_user_id = :authUserId OR qgr.query_group_id IN (:groupIds)")
    Mono<Long> countOwnedOrShared(Long authUserId, String tableName, List<Long> groupIds);

    @Query("SELECT DISTINCT e.* FROM ems_user_course_purchase e " +
           "LEFT JOIN record_owner ro ON ro.table_name = :tableName AND ro.record_id = e.usercoursepurchase_id " +
           "LEFT JOIN query_group_record qgr ON qgr.table_name = :tableName AND qgr.record_id = e.usercoursepurchase_id " +
           "WHERE ro.auth_user_id = :authUserId OR qgr.query_group_id IN (:groupIds) " +
           "LIMIT :limit OFFSET :offset")
    Flux<UserCoursePurchase> findAllPagedOwnedOrShared(Long authUserId, String tableName, List<Long> groupIds, int limit, long offset);

}