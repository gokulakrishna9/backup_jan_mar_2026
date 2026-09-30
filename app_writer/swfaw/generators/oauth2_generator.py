"""Generator for OAuth2 authentication components."""

from jinja2 import Template
from templates.oauth2_templates import (
    OAUTH2_PROVIDER_ENTITY,
    OAUTH2_LINKED_ACCOUNT_ENTITY,
    OAUTH2_PROVIDER_REPOSITORY,
    OAUTH2_LINKED_ACCOUNT_REPOSITORY,
    OAUTH2_SERVICE,
    OAUTH2_CONTROLLER
)


class OAuth2Generator:
    """Generates OAuth2 authentication components."""
    
    @staticmethod
    def generate_oauth2_provider_entity(package_name: str) -> str:
        """Generate OAuth2Provider entity."""
        template = Template(OAUTH2_PROVIDER_ENTITY)
        return template.render(
            entityPackage=f"{package_name}.entity"
        )
    
    @staticmethod
    def generate_oauth2_linked_account_entity(package_name: str) -> str:
        """Generate OAuth2LinkedAccount entity."""
        template = Template(OAUTH2_LINKED_ACCOUNT_ENTITY)
        return template.render(
            entityPackage=f"{package_name}.entity"
        )
    
    @staticmethod
    def generate_oauth2_provider_repository(package_name: str) -> str:
        """Generate OAuth2ProviderRepository."""
        template = Template(OAUTH2_PROVIDER_REPOSITORY)
        return template.render(
            repositoryPackage=f"{package_name}.repository",
            entityPackage=f"{package_name}.entity"
        )
    
    @staticmethod
    def generate_oauth2_linked_account_repository(package_name: str) -> str:
        """Generate OAuth2LinkedAccountRepository."""
        template = Template(OAUTH2_LINKED_ACCOUNT_REPOSITORY)
        return template.render(
            repositoryPackage=f"{package_name}.repository",
            entityPackage=f"{package_name}.entity"
        )
    
    @staticmethod
    def generate_oauth2_service(package_name: str) -> str:
        """Generate OAuth2Service."""
        template = Template(OAUTH2_SERVICE)
        return template.render(
            servicePackage=f"{package_name}.service",
            entityPackage=f"{package_name}.entity",
            repositoryPackage=f"{package_name}.repository"
        )
    
    @staticmethod
    def generate_oauth2_controller(package_name: str) -> str:
        """Generate OAuth2Controller."""
        template = Template(OAUTH2_CONTROLLER)
        return template.render(
            controllerPackage=f"{package_name}.controller",
            servicePackage=f"{package_name}.service",
            entityPackage=f"{package_name}.entity",
            authPackage=f"{package_name}.auth"
        )
