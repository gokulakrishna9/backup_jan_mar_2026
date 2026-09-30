package com.onlineshopping.dto;

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