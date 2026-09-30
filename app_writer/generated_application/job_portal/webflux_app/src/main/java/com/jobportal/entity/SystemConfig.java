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
@Table("system_config")
public class SystemConfig {
    
    @Id
    private String configKey;
    private String configValue;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}