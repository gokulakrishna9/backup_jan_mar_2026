"""Exception generator for code generation."""

from jinja2 import Template
from templates.exception_templates import ExceptionTemplates
from templates.dto_templates import DTOTemplates


class ExceptionGenerator:
    """Generator for exception handling classes."""
    
    @staticmethod
    def generate_page_response(package_name: str) -> str:
        """Generate PageResponse<T> generic DTO class.
        
        Args:
            package_name: Java package name
            
        Returns:
            Generated Java code
        """
        template = Template(DTOTemplates.PAGE_RESPONSE_TEMPLATE)
        return template.render(packageName=f"{package_name}.dto")
    
    @staticmethod
    def generate_global_exception_handler(package_name: str) -> str:
        """Generate GlobalExceptionHandler class.
        
        Args:
            package_name: Java package name
            
        Returns:
            Generated Java code
        """
        template = Template(ExceptionTemplates.GLOBAL_EXCEPTION_HANDLER_TEMPLATE)
        return template.render(packageName=f"{package_name}.exception")
    
    @staticmethod
    def generate_error_response(package_name: str) -> str:
        """Generate ErrorResponse class.
        
        Args:
            package_name: Java package name
            
        Returns:
            Generated Java code
        """
        template = Template(ExceptionTemplates.ERROR_RESPONSE_TEMPLATE)
        return template.render(packageName=f"{package_name}.exception")
    
    @staticmethod
    def generate_validation_error_response(package_name: str) -> str:
        """Generate ValidationErrorResponse class.
        
        Args:
            package_name: Java package name
            
        Returns:
            Generated Java code
        """
        template = Template(ExceptionTemplates.VALIDATION_ERROR_RESPONSE_TEMPLATE)
        return template.render(packageName=f"{package_name}.exception")
    
    @staticmethod
    def generate_entity_not_found_exception(package_name: str) -> str:
        """Generate EntityNotFoundException class.
        
        Args:
            package_name: Java package name
            
        Returns:
            Generated Java code
        """
        template = Template(ExceptionTemplates.ENTITY_NOT_FOUND_EXCEPTION_TEMPLATE)
        return template.render(packageName=f"{package_name}.exception")
    
    @staticmethod
    def generate_access_denied_exception(package_name: str) -> str:
        """Generate AccessDeniedException class.
        
        Args:
            package_name: Java package name
            
        Returns:
            Generated Java code
        """
        template = Template(ExceptionTemplates.ACCESS_DENIED_EXCEPTION_TEMPLATE)
        return template.render(packageName=f"{package_name}.exception")
    
    @staticmethod
    def generate_duplicate_entity_exception(package_name: str) -> str:
        """Generate DuplicateEntityException class.
        
        Args:
            package_name: Java package name
            
        Returns:
            Generated Java code
        """
        template = Template(ExceptionTemplates.DUPLICATE_ENTITY_EXCEPTION_TEMPLATE)
        return template.render(packageName=f"{package_name}.exception")
