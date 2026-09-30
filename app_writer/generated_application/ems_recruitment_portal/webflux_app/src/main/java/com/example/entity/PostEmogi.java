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
 * Entity class for ems_post_emogi table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_post_emogi")
public class PostEmogi {
    
    @Id
    @Column("emogi_id")
    private Long emogiId;
    
    @Column("name")
    private String name;
    
    @Column("description")
    private String description;
    
    @Column("file_location")
    private String fileLocation;
    
}