"""Test templates for code generation."""


class TestTemplates:
    """Templates for test class generation."""
    
    TEST_TEMPLATE = """package {{ packageName }};

import {{ entityPackage }}.{{ entityName }};
import {{ servicePackage }}.{{ serviceName }};
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

/**
 * Unit tests for {{ serviceName }}.
 */
@ExtendWith(MockitoExtension.class)
public class {{ className }} {
    
    @Mock
    private {{ entityName }}Repository repository;
    
    @InjectMocks
    private {{ serviceName }} service;
    
    @Test
    public void testFindById() {
        // TODO: Implement test
    }
    
    @Test
    public void testCreate() {
        // TODO: Implement test
    }
    
    @Test
    public void testUpdate() {
        // TODO: Implement test
    }
    
    @Test
    public void testDelete() {
        // TODO: Implement test
    }
}
"""
