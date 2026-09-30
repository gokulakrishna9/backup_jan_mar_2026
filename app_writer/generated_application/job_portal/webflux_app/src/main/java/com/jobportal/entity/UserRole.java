package com.jobportal.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("user_role")
public class UserRole {
    
    @Id
    private Long userRoleId;
    private Long authUserId;
    private String role;
    private String tableName;
    private LocalDateTime grantedAt;
    private Long grantedByAuthUserId;
}