package com.example.entity;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;
import java.util.UUID;

/**
 * Entity class for ems_institution_department table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_institution_department")
public class InstitutionDepartment {
    
    @Id
    @Column("department_id")
    private Long departmentId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("department_name")
    private String departmentName;
    
    @Column("description")
    private String description;
    
    @Column("head_of_department_user_id")
    private Long headOfDepartmentUserId;
    
    @Column("contact_email")
    private String contactEmail;
    
    @Column("contact_phone")
    private String contactPhone;
    
    @Column("is_active")
    private Byte isActive;
    
}