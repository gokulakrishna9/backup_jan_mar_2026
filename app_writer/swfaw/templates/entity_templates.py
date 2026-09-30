"""Entity templates for code generation."""


class EntityTemplates:
    """Templates for entity class generation."""
    
    ENTITY_TEMPLATE = """package {{ packageName }};

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
 * Entity class for {{ tableName }} table.
{% if isRootEntity %} * Root entity with authorization support.
{% endif %}{% if parentEntity %} * Sub-entity of {{ parentEntity }}.
{% endif %} */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "{{ tableName }}")
public class {{ className }} {
    
{% for field in regularFields %}{% if field.isPrimaryKey %}    @Id
{% endif %}    @Column("{{ field.columnName }}")
    private {{ field.javaType }} {{ field.fieldName }};
    
{% endfor %}{% if hasAuditFields %}    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
{% endif %}{% if hasSoftDelete %}    @Column("deleted_at")
    private LocalDateTime deletedAt;
    
{% endif %}}
"""
