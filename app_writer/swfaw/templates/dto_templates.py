"""DTO templates for code generation."""


class DTOTemplates:
    """Templates for DTO class generation."""
    
    INPUT_DTO_TEMPLATE = """package {{ packageName }};

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for {{ entityName }} creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {{ className }} {
    
{% for fieldConfig in fieldConfigs %}{% if fieldConfig.includeInDTO %}{% set validation = fieldConfig.get('validation', {}) %}{% if validation.required %}    @NotNull(message = "{{ validation.get('requiredMessage', fieldConfig.fieldName + ' is required') }}")
{% endif %}{% if validation.email %}    @Email(message = "{{ validation.get('emailMessage', 'Invalid email format') }}")
{% endif %}{% if validation.minLength %}    @Size(min = {{ validation.minLength }}{% if validation.maxLength %}, max = {{ validation.maxLength }}{% endif %}, message = "{{ validation.get('minLengthMessage', fieldConfig.fieldName + ' length is invalid') }}")
{% elif validation.maxLength %}    @Size(max = {{ validation.maxLength }}, message = "{{ validation.get('maxLengthMessage', fieldConfig.fieldName + ' is too long') }}")
{% endif %}{% if validation.pattern %}    @Pattern(regexp = "{{ validation.pattern }}", message = "{{ validation.get('patternMessage', fieldConfig.fieldName + ' format is invalid') }}")
{% endif %}{% if validation.min is defined %}    @Min(value = {{ validation.min }}, message = "{{ validation.get('minMessage', fieldConfig.fieldName + ' is too small') }}")
{% endif %}{% if validation.max is defined %}    @Max(value = {{ validation.max }}, message = "{{ validation.get('maxMessage', fieldConfig.fieldName + ' is too large') }}")
{% endif %}    private {{ fieldConfig.javaType }} {{ fieldConfig.fieldName }};
    
{% endif %}{% endfor %}{% if hasPublicFlag %}    private Boolean isPublic;  // Optional, defaults to false
{% endif %}{% if customValidators %}{% for validator in customValidators %}    // Custom validator: {{ validator.validatorClass }}
{% endfor %}{% endif %}}
"""
    
    OUTPUT_DTO_TEMPLATE = """package {{ packageName }};

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
{% if includeRelationships %}import com.fasterxml.jackson.annotation.JsonInclude;
{% endif %}import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for {{ entityName }} responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
{% if includeRelationships %}@JsonInclude(JsonInclude.Include.NON_NULL)
{% endif %}public class {{ className }} {
    
{% for fieldConfig in fieldConfigs %}{% if fieldConfig.includeInDTO and fieldConfig.fieldName not in excludeSensitiveFields %}{% if fieldConfig.get('format') %}    // Format: {{ fieldConfig.format }}
{% endif %}    private {{ fieldConfig.javaType }} {{ fieldConfig.fieldName }};
    
{% endif %}{% endfor %}{% if hasAuditFields %}    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
{% endif %}{% if includeRelationships %}    // Related entities can be included here
{% endif %}}
"""
    
    FILTER_DTO_TEMPLATE = """package {{ packageName }};

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for {{ entityName }} search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {{ className }} {
    
{% for fieldConfig in fieldConfigs %}{% if fieldConfig.includeInDTO %}    // Filter type: {{ fieldConfig.get('filterType', 'EQUALS') }}
    private {{ fieldConfig.javaType }} {{ fieldConfig.fieldName }};
    
{% endif %}{% endfor %}    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
"""

    PAGE_RESPONSE_TEMPLATE = '''package {{ packageName }};

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.List;

/**
 * Generic page response wrapper compatible with Spring Page shape.
 * Used by all paginated endpoints.
 *
 * @param <T> the type of content elements
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Paginated response wrapper")
public class PageResponse<T> {

    @Schema(description = "Page content")
    private List<T> content;

    @Schema(description = "Total number of elements across all pages")
    private long totalElements;

    @Schema(description = "Current page number (zero-based)")
    private int number;

    @Schema(description = "Page size")
    private int size;

    @Schema(description = "Total number of pages")
    private int totalPages;

    /**
     * Convenience factory for building a PageResponse from a list slice.
     */
    public static <T> PageResponse<T> of(List<T> content, long totalElements, int page, int size) {
        return PageResponse.<T>builder()
                .content(content)
                .totalElements(totalElements)
                .number(page)
                .size(size)
                .totalPages(size > 0 ? (int) Math.ceil((double) totalElements / size) : 0)
                .build();
    }
}
'''
