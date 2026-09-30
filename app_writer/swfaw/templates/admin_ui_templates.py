"""Admin UI templates for user and authorization management."""


class AdminUITemplates:
    """Templates for admin UI generation."""
    
    # Admin Service
    ADMIN_SERVICE = """package {{ packageName }};

import {{ entityPackage }}.AuthUser;
import {{ entityPackage }}.UserRole;
import {{ entityPackage }}.QueryGroup;
import {{ entityPackage }}.QueryGroupMember;
import {{ repositoryPackage }}.AuthUserRepository;
import {{ repositoryPackage }}.UserRoleRepository;
import {{ repositoryPackage }}.QueryGroupRepository;
import {{ repositoryPackage }}.QueryGroupMemberRepository;
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
"""

    # Admin Controller
    ADMIN_CONTROLLER = """package {{ packageName }};

import {{ servicePackage }}.AdminService;
import {{ entityPackage }}.*;
import {{ securityPackage }}.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;

@Controller
@RequestMapping("/admin")
@RequiredArgsConstructor
public class AdminController {
    
    private final AdminService adminService;
    
    /**
     * Check if current user is admin (has SUPER_ADMIN role)
     */
    private Mono<Boolean> isAdmin() {
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> adminService.getUserRoles(user.getAuthUserId())
                .any(role -> "SUPER_ADMIN".equals(role.getRole())))
            .defaultIfEmpty(false);
    }

    /**
     * Check auth and redirect to login if not authenticated
     */
    private Mono<String> requireAdmin(java.util.function.Supplier<Mono<String>> action) {
        return SecurityContextHolder.getCurrentUser()
            .switchIfEmpty(Mono.error(new RuntimeException("unauthenticated")))
            .flatMap(user -> adminService.getUserRoles(user.getAuthUserId())
                .any(role -> "SUPER_ADMIN".equals(role.getRole()))
                .flatMap(isAdmin -> isAdmin ? action.get()
                    : Mono.just("redirect:/login?error=access_denied")))
            .onErrorResume(e -> Mono.just("redirect:/login?message=Please+login+to+access+admin"));
    }
    
    // ========== Dashboard ==========
    
    @GetMapping
    public Mono<String> dashboard(Model model) {
        return requireAdmin(() ->
            SecurityContextHolder.getCurrentUser()
                .doOnNext(user -> model.addAttribute("currentUser", user))
                .thenReturn("admin/dashboard")
        );
    }
    
    @GetMapping("/dashboard")
    public Mono<String> dashboardExplicit(Model model) {
        return dashboard(model);
    }
    
    // ========== User Management ==========
    
    @GetMapping("/users")
    public Mono<String> listUsers(Model model) {
        return requireAdmin(() ->
            adminService.getAllUsers()
                .collectList()
                .doOnNext(users -> model.addAttribute("users", users))
                .thenReturn("admin/users")
        );
    }
    
    @GetMapping("/users/{id}")
    public Mono<String> viewUser(@PathVariable Long id, Model model) {
        return requireAdmin(() ->
            adminService.getUserById(id)
                .doOnNext(user -> model.addAttribute("user", user))
                .then(adminService.getUserRoles(id).collectList())
                .doOnNext(roles -> model.addAttribute("userRoles", roles))
                .thenReturn("admin/user-detail")
        );
    }
    
    // ========== Query Group Management ==========
    
    @GetMapping("/groups")
    public Mono<String> listGroups(Model model) {
        return requireAdmin(() ->
            adminService.getAllQueryGroups()
                .collectList()
                .doOnNext(groups -> model.addAttribute("groups", groups))
                .thenReturn("admin/groups")
        );
    }
    
    @GetMapping("/groups/{id}")
    public Mono<String> viewGroup(@PathVariable Long id, Model model) {
        return requireAdmin(() ->
            adminService.getQueryGroupById(id)
                .doOnNext(group -> model.addAttribute("group", group))
                .then(adminService.getQueryGroupMembers(id).collectList())
                .doOnNext(members -> model.addAttribute("members", members))
                .thenReturn("admin/document-groups")
        );
    }
}
"""
