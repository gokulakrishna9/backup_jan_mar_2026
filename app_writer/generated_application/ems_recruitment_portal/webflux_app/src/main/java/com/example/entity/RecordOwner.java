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
@Table("record_owner")
public class RecordOwner {
    
    @Id
    private Long recordOwnerId;
    private Long authUserId;
    private String tableName;
    private Long recordId;
    private LocalDateTime createdAt;
}