"""Custom query templates for code generation."""


class CustomQueryTemplates:
    """Templates for custom query repository, service, and controller generation."""
    
    # Template for Query Result DTO
    QUERY_RESULT_DTO_TEMPLATE = """package {{ packageName }};

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
{% for import in imports %}
import {{ import }};
{% endfor %}

/**
 * DTO for {{ queryName }} query results.
 * {{ description }}
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {{ className }} {
{% for field in fields %}
    private {{ field.type }} {{ field.name }};
{% endfor %}
}
"""
    
    # Template for Custom Query Repository
    CUSTOM_QUERY_REPOSITORY_TEMPLATE = """package {{ packageName }};

import org.springframework.r2dbc.core.DatabaseClient;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.util.HashMap;
import java.util.Map;
{% for import in imports %}
import {{ import }};
{% endfor %}

/**
 * Custom query repository for {{ entityName }}.
 * Contains pre-built queries using R2DBC DatabaseClient.
 */
@Repository
public class {{ className }} {
    
    private final DatabaseClient databaseClient;
    
    public {{ className }}(DatabaseClient databaseClient) {
        this.databaseClient = databaseClient;
    }
{% for query in queries %}
    
    /**
     * {{ query.description }}
     {% if query.parameters %}* Parameters:
     {% for param in query.parameters %}* @param {{ param.name }} {{ param.type }}{% if param.required %} (required){% else %} (optional){% endif %}
     {% endfor %}{% endif %}{% if query.pagination %}* @param page Page number (0-indexed)
     * @param size Page size
     {% endif %}* @return {{ query.returnType }}
     */
    public {% if query.pagination %}Flux{% else %}Flux{% endif %}<{{ query.returnType }}> {{ query.name }}(
        {%- for param in query.parameters -%}
        {{ param.type }} {{ param.name }}{% if not loop.last %}, {% endif %}
        {%- endfor -%}
        {%- if query.pagination -%}
        {% if query.parameters %}, {% endif %}int page, int size
        {%- endif -%}
    ) {
        String sql = "{{ query.sql }}";
        {% if query.pagination %}
        sql += " LIMIT :limit OFFSET :offset";
        {% endif %}
        
        DatabaseClient.GenericExecuteSpec spec = databaseClient.sql(sql);
        {% for param in query.parameters %}
        {% if param.required %}
        spec = spec.bind("{{ param.name }}", {{ param.name }});
        {% else %}
        if ({{ param.name }} != null) {
            spec = spec.bind("{{ param.name }}", {{ param.name }});
        }{% if param.defaultValue %} else {
            spec = spec.bind("{{ param.name }}", {{ param.defaultValue }});
        }{% endif %}
        {% endif %}
        {% endfor %}
        {% if query.pagination %}
        spec = spec.bind("limit", size);
        spec = spec.bind("offset", page * size);
        {% endif %}
        
        return spec.map((row, metadata) -> {
            {{ query.returnType }}.{{ query.returnType }}Builder builder = {{ query.returnType }}.builder();
            {% for field in query.resultFields %}
            builder.{{ field.name }}(row.get("{{ field.columnName }}", {{ field.type }}.class));
            {% endfor %}
            return builder.build();
        }).all();
    }
    {% if query.pagination %}
    
    /**
     * Count total results for {{ query.name }}.
     {% if query.parameters %}* Parameters:
     {% for param in query.parameters %}* @param {{ param.name }} {{ param.type }}{% if param.required %} (required){% else %} (optional){% endif %}
     {% endfor %}{% endif %}* @return Total count
     */
    public Mono<Long> count{{ query.name | capitalize }}(
        {%- for param in query.parameters -%}
        {{ param.type }} {{ param.name }}{% if not loop.last %}, {% endif %}
        {%- endfor -%}
    ) {
        String sql = "{{ query.countSql }}";
        
        DatabaseClient.GenericExecuteSpec spec = databaseClient.sql(sql);
        {% for param in query.parameters %}
        {% if param.required %}
        spec = spec.bind("{{ param.name }}", {{ param.name }});
        {% else %}
        if ({{ param.name }} != null) {
            spec = spec.bind("{{ param.name }}", {{ param.name }});
        }{% if param.defaultValue %} else {
            spec = spec.bind("{{ param.name }}", {{ param.defaultValue }});
        }{% endif %}
        {% endif %}
        {% endfor %}
        
        return spec.map((row, metadata) -> row.get(0, Long.class))
            .one()
            .defaultIfEmpty(0L);
    }
    {% endif %}
{% endfor %}
}
"""

    
    # Template for Custom Query Service
    CUSTOM_QUERY_SERVICE_TEMPLATE = """package {{ packageName }};

import {{ repositoryPackage }}.{{ repositoryName }};
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
{% for import in imports %}
import {{ import }};
{% endfor %}

/**
 * Service for custom queries on {{ entityName }}.
 */
@Service
public class {{ className }} {
    
    private final {{ repositoryName }} repository;
    
    public {{ className }}(
        {{ repositoryName }} repository
    ) {
        this.repository = repository;
    }
{% for query in queries %}
    
    /**
     * {{ query.description }}
     {% if query.parameters %}* Parameters:
     {% for param in query.parameters %}* @param {{ param.name }} {{ param.type }}{% if param.required %} (required){% else %} (optional){% endif %}
     {% endfor %}{% endif %}{% if query.pagination %}* @param page Page number (0-indexed)
     * @param size Page size
     {% endif %}{% if query.authorization.enabled %}* @param authUserId Authenticated user ID
     {% endif %}* @return {{ query.returnType }}
     */
    public {% if query.pagination %}Flux{% else %}Flux{% endif %}<{{ query.returnType }}> {{ query.name }}(
        {%- for param in query.parameters -%}
        {{ param.type }} {{ param.name }}, 
        {%- endfor -%}
        {%- if query.pagination -%}
        int page, int size{% if query.authorization.enabled %}, {% endif %}
        {%- endif -%}
        {%- if query.authorization.enabled -%}
        Long authUserId
        {%- endif -%}
    ) {
        return repository.{{ query.name }}(
            {%- for param in query.parameters -%}
            {{ param.name }}{% if not loop.last %}, {% endif %}
            {%- endfor -%}
            {%- if query.pagination -%}
            {% if query.parameters %}, {% endif %}page, size
            {%- endif -%}
        );
    }
    {% if query.pagination %}
    
    /**
     * Count total results for {{ query.name }}.
     {% if query.parameters %}* Parameters:
     {% for param in query.parameters %}* @param {{ param.name }} {{ param.type }}{% if param.required %} (required){% else %} (optional){% endif %}
     {% endfor %}{% endif %}* @return Total count
     */
    public Mono<Long> count{{ query.name | capitalize }}(
        {%- for param in query.parameters -%}
        {{ param.type }} {{ param.name }}{% if not loop.last %}, {% endif %}
        {%- endfor -%}
    ) {
        return repository.count{{ query.name | capitalize }}(
            {%- for param in query.parameters -%}
            {{ param.name }}{% if not loop.last %}, {% endif %}
            {%- endfor -%}
        );
    }
    {% endif %}
{% endfor %}
}
"""

    
    # Template for Custom Query Controller
    CUSTOM_QUERY_CONTROLLER_TEMPLATE = """package {{ packageName }};

import {{ servicePackage }}.{{ serviceName }};
import {{ dtoPackage }}.{{ filterDtoName }};
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
{% for import in imports %}
import {{ import }};
{% endfor %}

/**
 * REST Controller for custom queries on {{ entityName }}.
 */
@RestController
@RequestMapping("{{ basePath }}")
@Tag(name = "{{ entityName }} Custom Queries", description = "Custom query endpoints for {{ entityName }}")
public class {{ className }} {
    
    private final {{ serviceName }} service;
    
    public {{ className }}({{ serviceName }} service) {
        this.service = service;
    }
{% for query in queries %}
    
    /**
     * {{ query.description }}
     */
    @{{ query.httpMethod }}("{{ query.path }}")
    @Operation(summary = "{{ query.description }}")
    public {% if query.pagination %}Mono<ResponseEntity<Flux<{{ query.returnType }}>>>{% else %}Flux<{{ query.returnType }}>{% endif %} {{ query.name }}(
        {%- for param in query.parameters -%}
        {% if param.pathVariable %}@PathVariable{% else %}@RequestParam{% if not param.required %}(required = false){% endif %}{% endif %} {{ param.type }} {{ param.name }}, 
        {%- endfor -%}
        {%- if query.pagination -%}
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size{% if query.authorization.enabled %}, {% endif %}
        {%- endif -%}
        {%- if query.authorization.enabled -%}
        Authentication authentication
        {%- endif -%}
    ) {
        {% if query.authorization.enabled %}
        Long authUserId = Long.parseLong(authentication.getName());
        {% endif %}
        {% if query.pagination %}
        Flux<{{ query.returnType }}> results = service.{{ query.name }}(
            {%- for param in query.parameters -%}
            {{ param.name }}, 
            {%- endfor -%}
            page, size{% if query.authorization.enabled %}, authUserId{% endif %}
        );
        
        Mono<Long> total = service.count{{ query.name | capitalize }}(
            {%- for param in query.parameters -%}
            {{ param.name }}{% if not loop.last %}, {% endif %}
            {%- endfor -%}
        );
        
        return total.map(count -> {
            return ResponseEntity.ok()
                .header("X-Total-Count", String.valueOf(count))
                .header("X-Page", String.valueOf(page))
                .header("X-Page-Size", String.valueOf(size))
                .body(results);
        });
        {% else %}
        return service.{{ query.name }}(
            {%- for param in query.parameters -%}
            {{ param.name }}{% if not loop.last %}, {% endif %}
            {%- endfor -%}
            {%- if query.authorization.enabled -%}
            {% if query.parameters %}, {% endif %}authUserId
            {%- endif -%}
        );
        {% endif %}
    }
{% endfor %}
}
"""
    
    # Template for Filter DTO
    FILTER_DTO_TEMPLATE = """package {{ packageName }};

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
{% for import in imports %}
import {{ import }};
{% endfor %}

/**
 * Filter DTO for {{ entityName }} custom queries.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {{ className }} {
{% for field in fields %}
    
    // {{ field.name }} filters
    {% for operator in field.operators %}
    {% if operator == 'equals' %}
    private {{ field.type }} {{ field.name }};
    {% elif operator == 'contains' %}
    private String {{ field.name }}Contains;
    {% elif operator == 'startsWith' %}
    private String {{ field.name }}StartsWith;
    {% elif operator == 'endsWith' %}
    private String {{ field.name }}EndsWith;
    {% elif operator == 'greaterThan' %}
    private {{ field.type }} {{ field.name }}GreaterThan;
    {% elif operator == 'lessThan' %}
    private {{ field.type }} {{ field.name }}LessThan;
    {% elif operator == 'between' %}
    private {{ field.type }} {{ field.name }}From;
    private {{ field.type }} {{ field.name }}To;
    {% elif operator == 'in' %}
    private List<{{ field.type }}> {{ field.name }}In;
    {% endif %}
    {% endfor %}
{% endfor %}
}
"""
