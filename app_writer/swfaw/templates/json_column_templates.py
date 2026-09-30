"""JSON column templates - templates for R2DBC JSON type converters and configuration."""


class JsonColumnTemplates:
    """Templates for JSON reading/writing converters and R2DBC conversions config."""

    @staticmethod
    def generate_json_reading_converter(package_name: str) -> str:
        """Generate JsonReadingConverter that converts String to JsonNode using ObjectMapper.readTree()."""
        return f"""package {package_name}.converter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.convert.converter.Converter;
import org.springframework.data.convert.ReadingConverter;

/**
 * R2DBC reading converter that deserializes JSON strings from MySQL JSON columns
 * into Jackson JsonNode objects.
 */
@ReadingConverter
public class JsonReadingConverter implements Converter<String, JsonNode> {{

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public JsonNode convert(String source) {{
        try {{
            return objectMapper.readTree(source);
        }} catch (JsonProcessingException e) {{
            throw new IllegalArgumentException("Failed to parse JSON", e);
        }}
    }}
}}
"""

    @staticmethod
    def generate_json_writing_converter(package_name: str) -> str:
        """Generate JsonWritingConverter that converts JsonNode to String using ObjectMapper.writeValueAsString()."""
        return f"""package {package_name}.converter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.convert.converter.Converter;
import org.springframework.data.convert.WritingConverter;

/**
 * R2DBC writing converter that serializes Jackson JsonNode objects
 * into JSON strings for MySQL JSON columns.
 */
@WritingConverter
public class JsonWritingConverter implements Converter<JsonNode, String> {{

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String convert(JsonNode source) {{
        try {{
            return objectMapper.writeValueAsString(source);
        }} catch (JsonProcessingException e) {{
            throw new IllegalArgumentException("Failed to serialize JSON", e);
        }}
    }}
}}
"""

    @staticmethod
    def generate_r2dbc_json_conversions_config(package_name: str) -> str:
        """Generate R2dbcJsonConversionsConfig that registers both JSON converters with R2DBC."""
        return f"""package {package_name}.converter;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.r2dbc.convert.R2dbcCustomConversions;
import org.springframework.data.r2dbc.dialect.MySqlDialect;

import java.util.List;

/**
 * Configuration bean that registers the JsonReadingConverter and JsonWritingConverter
 * with R2DBC custom conversions, enabling automatic JSON column mapping.
 */
@Configuration
public class R2dbcJsonConversionsConfig {{

    @Bean
    public R2dbcCustomConversions r2dbcCustomConversions() {{
        return R2dbcCustomConversions.of(
            MySqlDialect.INSTANCE,
            List.of(
                new JsonReadingConverter(),
                new JsonWritingConverter()
            )
        );
    }}
}}
"""
