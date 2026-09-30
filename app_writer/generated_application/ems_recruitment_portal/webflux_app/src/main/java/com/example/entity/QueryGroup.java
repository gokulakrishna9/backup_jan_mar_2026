package com.example.entity;

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
@Table("query_group")
public class QueryGroup {
    
    @Id
    private Long queryGroupId;
    private String groupName;
    private String groupType;
    private Long ownerAuthUserId;
    private String description;
    private LocalDateTime createdAt;
}