package com.jobportal.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("query_group_query")
public class QueryGroupQuery {
    
    @Id
    private Long queryGroupQueryId;
    private Long queryGroupId;
    private String queryName;
}