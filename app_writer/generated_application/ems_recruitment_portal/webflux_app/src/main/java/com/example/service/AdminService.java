package com.example.service;

import com.example.entity.AuthUser;
import com.example.entity.UserRole;
import com.example.entity.QueryGroup;
import com.example.entity.QueryGroupMember;
import com.example.repository.AuthUserRepository;
import com.example.repository.UserRoleRepository;
import com.example.repository.QueryGroupRepository;
import com.example.repository.QueryGroupMemberRepository;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;

@Slf4j
@Service
@RequiredArgsConstructor
public class AdminService {
    
    private final AuthUserRepository authUserRepository;
    private final UserRoleRepository userRoleRepository;
    private final QueryGroupRepository queryGroupRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    
    // ========== User Management ==========
    
    public Flux<AuthUser> getAllUsers() {
        return authUserRepository.findAll();
    }
    
    public Mono<AuthUser> getUserById(Long userId) {
        return authUserRepository.findById(userId);
    }
    
    // ========== Role Management ==========
    
    public Flux<UserRole> getUserRoles(Long userId) {
        return userRoleRepository.findByAuthUserId(userId);
    }
    
    public Mono<UserRole> grantRole(Long userId, String role, String tableName, Long grantedBy) {
        UserRole userRole = UserRole.builder()
            .authUserId(userId)
            .role(role)
            .tableName(tableName)
            .grantedAt(LocalDateTime.now())
            .grantedByAuthUserId(grantedBy)
            .build();
        return userRoleRepository.save(userRole);
    }
    
    public Mono<Void> revokeRole(Long userRoleId) {
        return userRoleRepository.deleteById(userRoleId);
    }
    
    // ========== Query Group Management ==========
    
    public Flux<QueryGroup> getAllQueryGroups() {
        return queryGroupRepository.findAll();
    }
    
    public Mono<QueryGroup> getQueryGroupById(Long groupId) {
        return queryGroupRepository.findById(groupId);
    }
    
    public Flux<QueryGroupMember> getQueryGroupMembers(Long groupId) {
        return queryGroupMemberRepository.findByQueryGroupId(groupId);
    }
    
    public Mono<QueryGroupMember> addMemberToQueryGroup(Long groupId, Long userId) {
        QueryGroupMember member = QueryGroupMember.builder()
            .queryGroupId(groupId)
            .authUserId(userId)
            .joinedAt(LocalDateTime.now())
            .build();
        return queryGroupMemberRepository.save(member);
    }
    
    public Mono<Void> removeMemberFromQueryGroup(Long memberId) {
        return queryGroupMemberRepository.deleteById(memberId);
    }
}