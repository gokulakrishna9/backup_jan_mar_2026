package com.onlineshopping.entity;

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
@Table("query_group_record")
public class QueryGroupRecord {
    
    @Id
    private Long queryGroupRecordId;
    private Long queryGroupId;
    private String tableName;
    private Long recordId;
    private Long addedByAuthUserId;
    private LocalDateTime addedAt;
}