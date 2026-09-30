"""Generate layer definition files from DatabaseDefinition.

This module creates detailed layer definition JSON files that users can modify
before Phase 2 code generation.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from models.database_definition import DatabaseDefinition, Table
from transformers.entity_transformer import EntityTransformer
from transformers.repository_transformer import RepositoryTransformer
from transformers.service_transformer import ServiceTransformer
from transformers.controller_transformer import ControllerTransformer
from transformers.dto_transformer import DTOTransformer
from transformers.query_transformer import QueryTransformer
from transformers.default_query_transformer import DefaultQueryTransformer
from transformers.filter_transformer import FilterTransformer
from utils.string_utils import to_pascal_case, to_camel_case


def generate_entity_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate entity layer definition from database definition.
    
    Creates one entity configuration per table with defaults.
    """
    entities = []
    
    for table in db_def.tables:
        # Use existing transformer to get defaults
        entity_obj = EntityTransformer.transform(table, db_def.projectMetadata.groupId)
        
        # Convert to layer definition format
        entity_def = {
            "tableName": entity_obj.tableName,
            "className": entity_obj.className,
            "packageName": entity_obj.packageName,
            "fields": [
                {
                    "columnName": field.columnName,
                    "fieldName": field.fieldName,
                    "javaType": field.javaType,
                    "isPrimaryKey": field.isPrimaryKey,
                    "isNullable": field.isNullable,
                    "columnDefinition": field.columnDefinition
                }
                for field in entity_obj.fields
            ],
            "isRootEntity": entity_obj.isRootEntity,
            "parentEntity": entity_obj.parentEntity,
            "hasPublicFlag": entity_obj.hasPublicFlag,
            "hasAuditFields": entity_obj.hasAuditFields,
            "hasSoftDelete": entity_obj.hasSoftDelete
        }
        entities.append(entity_def)
    
    return {
        "layerType": "entity",
        "description": "Entity layer configuration - controls JPA entity generation with R2DBC support",
        "entities": entities,
        "globalSettings": {
            "defaultAuditFields": True,
            "defaultSoftDelete": True,
            "auditFieldNames": {
                "createdAt": "created_at",
                "updatedAt": "updated_at",
                "createdBy": "created_by",
                "updatedBy": "updated_by"
            },
            "softDeleteFieldName": "deleted_at"
        }
    }


def generate_repository_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate repository layer definition from database definition."""
    repositories = []
    
    for table in db_def.tables:
        # First transform to entity, then to repository
        entity_obj = EntityTransformer.transform(table, db_def.projectMetadata.groupId)
        repo_obj = RepositoryTransformer.transform(entity_obj)
        
        repo_def = {
            "entityName": repo_obj.entityName,
            "className": repo_obj.className,
            "packageName": repo_obj.packageName,
            "idType": repo_obj.idType,
            "hasCustomQueries": repo_obj.hasCustomQueries,
            "customQueries": repo_obj.customQueries,
            "hasSoftDelete": repo_obj.hasSoftDelete,
            "hasAuthorization": repo_obj.hasAuthorization,
            "enableCaching": False,  # Future: Redis/in-memory caching support
            "cacheNames": []  # Future: Cache names for @Cacheable annotations
        }
        repositories.append(repo_def)
    
    return {
        "layerType": "repository",
        "description": "Repository layer configuration - controls R2DBC repository generation",
        "note": "Fields marked as 'Future' are placeholders for upcoming functionality",
        "repositories": repositories,
        "globalSettings": {
            "defaultSoftDeleteFilter": True,
            "defaultAuthorizationCheck": True,
            "baseRepositoryInterface": "ReactiveCrudRepository"
        }
    }


def generate_service_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate service layer definition from database definition."""
    services = []
    
    for table in db_def.tables:
        # First transform to entity, then to service
        entity_obj = EntityTransformer.transform(table, db_def.projectMetadata.groupId)
        service_obj = ServiceTransformer.transform(entity_obj)
        
        service_def = {
            "entityName": service_obj.entityName,
            "className": service_obj.className,
            "packageName": service_obj.packageName,
            "repositoryName": service_obj.repositoryName,
            "isRootEntity": service_obj.isRootEntity,
            "hasAuthorization": service_obj.hasAuthorization,
            "authorizationConfig": {  # Future: Fine-grained authorization control
                "checkOnCreate": True,
                "checkOnRead": True,
                "checkOnUpdate": True,
                "checkOnDelete": True,
                "allowPublicRead": False,
                "requireOwnership": True
            },
            "transactionManagement": {  # Future: Transaction configuration
                "enabled": True,
                "propagation": "REQUIRED",
                "isolation": "DEFAULT",
                "timeout": 30
            },
            "customMethods": [],  # Future: Custom business logic methods
            "validationRules": {  # Future: Custom validation rules
                "onCreate": [],
                "onUpdate": [],
                "onDelete": []
            }
        }
        services.append(service_def)
    
    return {
        "layerType": "service",
        "description": "Service layer configuration - controls business logic and authorization",
        "services": services,
        "globalSettings": {
            "defaultAuthorizationEnabled": True,
            "defaultTransactionEnabled": True,
            "auditServiceCalls": True
        }
    }


def generate_controller_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate controller layer definition from database definition."""
    controllers = []
    
    for table in db_def.tables:
        # First transform to entity, then to controller
        entity_obj = EntityTransformer.transform(table, db_def.projectMetadata.groupId)
        controller_obj = ControllerTransformer.transform(entity_obj)
        
        controller_def = {
            "entityName": controller_obj.entityName,
            "className": controller_obj.className,
            "packageName": controller_obj.packageName,
            "serviceName": controller_obj.serviceName,
            "basePath": controller_obj.basePath,
            "isRootEntity": controller_obj.isRootEntity,
            "endpoints": controller_obj.endpoints,
            "customEndpoints": controller_obj.customEndpoints,
            "corsConfig": controller_obj.corsConfig
        }
        controllers.append(controller_def)
    
    return {
        "layerType": "controller",
        "description": "Controller layer configuration - controls REST endpoint generation with fine-grained control",
        "controllers": controllers,
        "globalSettings": {
            "apiVersion": "v1",
            "defaultRateLimitPerMinute": 60,
            "enableSwagger": True,
            "enableCors": True
        }
    }


def generate_dto_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate DTO layer definition from database definition using transformer."""
    dtos = []
    
    for table in db_def.tables:
        # First transform to entity
        entity_obj = EntityTransformer.transform(table, db_def.projectMetadata.groupId)
        
        # Generate Input, Output, and Filter DTOs using transformer
        for dto_type in ['Input', 'Output', 'Filter']:
            dto_obj = DTOTransformer.transform(entity_obj, dto_type)
            
            dto_def = {
                "entityName": dto_obj.entityName,
                "dtoType": dto_obj.dtoType,
                "className": dto_obj.className,
                "packageName": dto_obj.packageName,
                "fields": dto_obj.fieldConfigs,  # Use fieldConfigs instead of fields
                "customValidators": dto_obj.customValidators,
                "excludeSensitiveFields": dto_obj.excludeSensitiveFields,
                "includeRelationships": dto_obj.includeRelationships
            }
            dtos.append(dto_def)
    
    return {
        "layerType": "dto",
        "description": "DTO layer configuration - controls Data Transfer Object generation with validation",
        "dtos": dtos,
        "globalSettings": {
            "generateInputDTO": True,
            "generateOutputDTO": True,
            "generateFilterDTO": True,
            "defaultValidationMessages": {
                "required": "{field} is required",
                "email": "Invalid email format",
                "min": "{field} must be at least {value}",
                "max": "{field} cannot exceed {value}",
                "pattern": "{field} format is invalid"
            }
        }
    }


def _map_sql_to_java(sql_type: str) -> str:
    """Map SQL type to Java type."""
    from utils.string_utils import map_sql_type_to_java
    return map_sql_type_to_java(sql_type)


def _generate_validation_rules(column) -> Dict[str, Any]:
    """Generate validation rules based on column definition."""
    validation = {}
    
    # Required validation
    if not column.nullable:
        validation["required"] = True
        validation["requiredMessage"] = f"{to_pascal_case(column.name)} is required"
    
    # String validations
    if column.type.upper().startswith('VARCHAR'):
        # Extract length from VARCHAR(255)
        if '(' in column.type:
            length = int(column.type.split('(')[1].split(')')[0])
            validation["maxLength"] = length
            validation["maxLengthMessage"] = f"{to_pascal_case(column.name)} cannot exceed {length} characters"
    
    # Email validation
    if 'email' in column.name.lower():
        validation["email"] = True
        validation["emailMessage"] = "Please provide a valid email address"
    
    return validation


def generate_all_layer_definitions(db_def: DatabaseDefinition, output_dir: str) -> Dict[str, str]:
    """Generate all layer definition files.
    
    Args:
        db_def: Database definition
        output_dir: Output directory for the application
        
    Returns:
        Dictionary mapping layer types to file paths
    """
    output_path = Path(output_dir)
    definitions_dir = output_path / 'application_definitions'
    definitions_dir.mkdir(parents=True, exist_ok=True)
    
    file_paths = {}
    
    # Generate each layer definition (per-entity and application-wide)
    layers = {
        # Per-entity layer definitions
        'entity_layer': generate_entity_layer_definition,
        'repository_layer': generate_repository_layer_definition,
        'service_layer': generate_service_layer_definition,
        'controller_layer': generate_controller_layer_definition,
        'dto_layer': generate_dto_layer_definition,
        'query_layer': generate_query_layer_definition,
        'filter_layer': generate_filter_layer_definition,
        # Application-wide layer definitions
        'security_layer': generate_security_layer_definition,
        'config_layer': generate_config_layer_definition,
        'exception_layer': generate_exception_layer_definition,
        'audit_logging_layer': generate_audit_logging_layer_definition,
        'authorization_layer': generate_authorization_layer_definition,
        'group_definition_layer': generate_group_definition_layer,
        'custom_queries_layer': generate_custom_queries_layer_definition,
    }
    
    for layer_name, generator_func in layers.items():
        layer_def = generator_func(db_def)
        layer_file = definitions_dir / f'webflux_{layer_name}.json'
        
        with open(layer_file, 'w', encoding='utf-8') as f:
            json.dump(layer_def, f, indent=2, ensure_ascii=False)
        
        file_paths[layer_name] = str(layer_file)
        print(f"   - Generated: webflux_{layer_name}.json")
    
    return file_paths
def generate_security_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate security layer definition from project metadata.

    Args:
        db_def: Database definition

    Returns:
        Security layer definition dictionary
    """
    project = db_def.projectMetadata

    return {
        "layerType": "security",
        "description": "Security configuration - JWT, OAuth2, password policies, CORS",
        "jwt": {
            "enabled": True,
            "secret": "your-secret-key-change-in-production-min-256-bits",
            "expiration": 86400000,
            "expirationUnit": "milliseconds",
            "issuer": project.name,
            "audience": f"{project.name}-users",
            "algorithm": "HS256",
            "refreshToken": {
                "enabled": True,
                "expiration": 604800000,
                "expirationUnit": "milliseconds"
            }
        },
        "oauth2": {
            "enabled": False,
            "providers": [
                {
                    "name": "google",
                    "clientId": "${GOOGLE_CLIENT_ID}",
                    "clientSecret": "${GOOGLE_CLIENT_SECRET}",
                    "redirectUri": f"http://localhost:{project.port}/login/oauth2/code/google",
                    "scope": ["email", "profile"]
                },
                {
                    "name": "github",
                    "clientId": "${GITHUB_CLIENT_ID}",
                    "clientSecret": "${GITHUB_CLIENT_SECRET}",
                    "redirectUri": f"http://localhost:{project.port}/login/oauth2/code/github",
                    "scope": ["user:email"]
                }
            ]
        },
        "passwordPolicy": {
            "minLength": 8,
            "maxLength": 128,
            "requireUppercase": True,
            "requireLowercase": True,
            "requireDigit": True,
            "requireSpecialChar": True,
            "specialChars": "!@#$%^&*()_+-=[]{}|;:,.<>?",
            "preventCommonPasswords": True,
            "passwordExpirationDays": 90,
            "passwordHistoryCount": 5
        },
        "sessionManagement": {
            "maxConcurrentSessions": 3,
            "sessionTimeout": 1800,
            "sessionTimeoutUnit": "seconds"
        },
        "cors": {
            "enabled": True,
            "allowedOrigins": ["http://localhost:3000", "http://localhost:4200"],
            "allowedMethods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allowedHeaders": ["Authorization", "Content-Type", "X-Requested-With"],
            "exposedHeaders": ["Authorization"],
            "allowCredentials": True,
            "maxAge": 3600
        },
        "csrf": {
            "enabled": False,
            "cookieName": "XSRF-TOKEN",
            "headerName": "X-XSRF-TOKEN"
        },
        "rateLimiting": {
            "enabled": True,
            "defaultLimitPerMinute": 60,
            "loginAttempts": {
                "maxAttempts": 5,
                "lockoutDurationMinutes": 15
            }
        },
        "publicEndpoints": [
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/forgot-password",
            "/swagger-ui.html",
            "/swagger-ui/**",
            "/v3/api-docs/**"
        ]
    }


def generate_config_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate config layer definition from project metadata.

    Args:
        db_def: Database definition

    Returns:
        Config layer definition dictionary
    """
    project = db_def.projectMetadata
    database = project.database

    return {
        "layerType": "config",
        "description": "Application configuration - database, server, logging, features",
        "project": {
            "name": project.name,
            "displayName": project.applicationName,
            "groupId": project.groupId,
            "artifactId": project.artifactId,
            "version": project.version,
            "packageName": project.groupId,
            "javaVersion": "17",
            "springBootVersion": "3.2.0"
        },
        "server": {
            "port": project.port,
            "contextPath": "/",
            "compression": {
                "enabled": True,
                "mimeTypes": ["application/json", "application/xml", "text/html", "text/xml", "text/plain"]
            },
            "http2": {
                "enabled": True
            },
            "ssl": {
                "enabled": False,
                "keyStore": "${SSL_KEY_STORE}",
                "keyStorePassword": "${SSL_KEY_STORE_PASSWORD}",
                "keyStoreType": "PKCS12"
            }
        },
        "database": {
            "type": database.type,
            "host": database.host,
            "port": database.port,
            "name": database.name,
            "username": database.username,
            "password": database.password,
            "r2dbc": {
                "pool": {
                    "initialSize": 10,
                    "maxSize": 50,
                    "maxIdleTime": "30m",
                    "maxLifeTime": "60m",
                    "maxAcquireTime": "3s",
                    "maxCreateConnectionTime": "3s"
                }
            },
            "showSql": False,
            "formatSql": True
        },
        "logging": {
            "level": {
                "root": "INFO",
                "application": "DEBUG",
                "springframework": "INFO",
                "hibernate": "WARN"
            },
            "pattern": {
                "console": "%d{yyyy-MM-dd HH:mm:ss} - %msg%n",
                "file": "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
            },
            "file": {
                "enabled": True,
                "name": "logs/application.log",
                "maxSize": "10MB",
                "maxHistory": 30,
                "totalSizeCap": "1GB"
            }
        },
        "features": {
            "swagger": {
                "enabled": True,
                "title": f"{project.applicationName} API",
                "description": f"API documentation for {project.applicationName}",
                "version": project.version,
                "contactName": "API Support",
                "contactEmail": "support@example.com"
            },
            "actuator": {
                "enabled": True,
                "basePath": "/actuator",
                "endpoints": ["health", "info", "metrics", "prometheus"]
            },
            "caching": {
                "enabled": False,
                "type": "redis",
                "redis": {
                    "host": "localhost",
                    "port": 6379,
                    "password": "",
                    "database": 0
                },
                "ttl": 3600
            },
            "email": {
                "enabled": False,
                "host": "smtp.gmail.com",
                "port": 587,
                "username": "${EMAIL_USERNAME}",
                "password": "${EMAIL_PASSWORD}",
                "from": "noreply@example.com",
                "tls": True
            }
        },
        "profiles": {
            "active": "dev",
            "available": ["dev", "test", "prod"]
        }
    }


def generate_exception_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate exception layer definition with defaults.

    Args:
        db_def: Database definition

    Returns:
        Exception layer definition dictionary
    """
    project = db_def.projectMetadata
    package_name = project.groupId

    # Generate entity-specific exception messages
    exception_messages = {}
    for table in db_def.tables:
        entity_name = to_pascal_case(table.name)
        exception_messages[entity_name] = f"{entity_name} not found with the provided ID"

    return {
        "layerType": "exception",
        "description": "Exception handling configuration - custom exceptions and error responses",
        "customExceptions": [
            {
                "className": "ResourceNotFoundException",
                "packageName": f"{package_name}.exception",
                "httpStatus": 404,
                "defaultMessage": "The requested resource was not found",
                "includeTimestamp": True,
                "includeStackTrace": False
            },
            {
                "className": "UnauthorizedException",
                "packageName": f"{package_name}.exception",
                "httpStatus": 401,
                "defaultMessage": "You are not authorized to access this resource",
                "includeTimestamp": True,
                "includeStackTrace": False
            },
            {
                "className": "ForbiddenException",
                "packageName": f"{package_name}.exception",
                "httpStatus": 403,
                "defaultMessage": "Access to this resource is forbidden",
                "includeTimestamp": True,
                "includeStackTrace": False
            },
            {
                "className": "ValidationException",
                "packageName": f"{package_name}.exception",
                "httpStatus": 400,
                "defaultMessage": "Validation failed for the provided data",
                "includeTimestamp": True,
                "includeStackTrace": False,
                "includeFieldErrors": True
            },
            {
                "className": "DuplicateResourceException",
                "packageName": f"{package_name}.exception",
                "httpStatus": 409,
                "defaultMessage": "A resource with the same identifier already exists",
                "includeTimestamp": True,
                "includeStackTrace": False
            },
            {
                "className": "BusinessLogicException",
                "packageName": f"{package_name}.exception",
                "httpStatus": 422,
                "defaultMessage": "Business logic validation failed",
                "includeTimestamp": True,
                "includeStackTrace": False
            }
        ],
        "errorResponseFormat": {
            "includeTimestamp": True,
            "includeStatus": True,
            "includeError": True,
            "includeMessage": True,
            "includePath": True,
            "includeStackTrace": False,
            "includeFieldErrors": True,
            "timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
        },
        "globalExceptionHandling": {
            "handleValidationErrors": True,
            "handleMethodArgumentNotValid": True,
            "handleConstraintViolation": True,
            "handleHttpMessageNotReadable": True,
            "handleAccessDenied": True,
            "handleAuthenticationError": True,
            "handleInternalServerError": True
        },
        "exceptionMessages": {
            "ResourceNotFoundException": exception_messages,
            "ValidationException": {
                "email": "Please provide a valid email address",
                "phone": "Please provide a valid phone number",
                "date": "Please provide a valid date in format YYYY-MM-DD"
            }
        },
        "logging": {
            "logExceptions": True,
            "logStackTrace": True,
            "logLevel": "ERROR"
        }
    }


def generate_audit_logging_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate audit logging layer definition with defaults.

    Args:
        db_def: Database definition

    Returns:
        Audit logging layer definition dictionary
    """
    # Get list of important entities (those with authorization enabled)
    important_entities = [to_pascal_case(table.name) for table in db_def.tables[:10]]  # First 10 as examples

    return {
        "layerType": "auditLogging",
        "description": "Audit logging configuration - tracks user actions and system events",
        "enabled": True,
        "auditEvents": {
            "authentication": {
                "enabled": True,
                "events": [
                    {
                        "eventType": "LOGIN_SUCCESS",
                        "logLevel": "INFO",
                        "message": "User {username} logged in successfully from IP {ipAddress}",
                        "includeUserAgent": True,
                        "includeLocation": False
                    },
                    {
                        "eventType": "LOGIN_FAILURE",
                        "logLevel": "WARN",
                        "message": "Failed login attempt for user {username} from IP {ipAddress}",
                        "includeUserAgent": True,
                        "includeLocation": False
                    },
                    {
                        "eventType": "LOGOUT",
                        "logLevel": "INFO",
                        "message": "User {username} logged out",
                        "includeUserAgent": False,
                        "includeLocation": False
                    },
                    {
                        "eventType": "PASSWORD_CHANGE",
                        "logLevel": "INFO",
                        "message": "User {username} changed their password",
                        "includeUserAgent": True,
                        "includeLocation": False
                    }
                ]
            },
            "dataAccess": {
                "enabled": True,
                "events": [
                    {
                        "eventType": "CREATE",
                        "logLevel": "INFO",
                        "message": "User {username} created {entityType} with ID {entityId}",
                        "includeEntityData": False,
                        "entities": important_entities
                    },
                    {
                        "eventType": "READ",
                        "logLevel": "DEBUG",
                        "message": "User {username} accessed {entityType} with ID {entityId}",
                        "includeEntityData": False,
                        "entities": []
                    },
                    {
                        "eventType": "UPDATE",
                        "logLevel": "INFO",
                        "message": "User {username} updated {entityType} with ID {entityId}",
                        "includeEntityData": True,
                        "includeChanges": True,
                        "entities": important_entities
                    },
                    {
                        "eventType": "DELETE",
                        "logLevel": "WARN",
                        "message": "User {username} deleted {entityType} with ID {entityId}",
                        "includeEntityData": True,
                        "entities": important_entities
                    }
                ]
            },
            "authorization": {
                "enabled": True,
                "events": [
                    {
                        "eventType": "ACCESS_DENIED",
                        "logLevel": "WARN",
                        "message": "User {username} was denied access to {resource}",
                        "includeReason": True
                    },
                    {
                        "eventType": "PERMISSION_CHANGE",
                        "logLevel": "INFO",
                        "message": "User {username} permissions were modified by {modifiedBy}",
                        "includeChanges": True
                    }
                ]
            },
            "systemEvents": {
                "enabled": True,
                "events": [
                    {
                        "eventType": "APPLICATION_START",
                        "logLevel": "INFO",
                        "message": "Application started"
                    },
                    {
                        "eventType": "APPLICATION_STOP",
                        "logLevel": "INFO",
                        "message": "Application stopped"
                    },
                    {
                        "eventType": "CONFIGURATION_CHANGE",
                        "logLevel": "WARN",
                        "message": "Configuration changed by {username}",
                        "includeChanges": True
                    }
                ]
            }
        },
        "storage": {
            "type": "database",
            "tableName": "audit_log",
            "retentionDays": 365,
            "archiveAfterDays": 90,
            "archiveLocation": "s3://audit-logs-archive"
        },
        "filtering": {
            "excludeUsers": ["system", "health-check"],
            "excludeEndpoints": ["/actuator/health", "/actuator/info"],
            "excludeReadOperations": True,
            "sensitiveFields": ["password", "encryptedPassword", "creditCard", "ssn"]
        },
        "format": {
            "timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",
            "includeRequestId": True,
            "includeSessionId": True,
            "includeCorrelationId": True
        },
        "alerting": {
            "enabled": True,
            "alerts": [
                {
                    "eventType": "MULTIPLE_LOGIN_FAILURES",
                    "threshold": 5,
                    "timeWindowMinutes": 15,
                    "action": "SEND_EMAIL",
                    "recipients": ["security@example.com"]
                },
                {
                    "eventType": "BULK_DELETE",
                    "threshold": 100,
                    "timeWindowMinutes": 5,
                    "action": "SEND_EMAIL",
                    "recipients": ["admin@example.com"]
                }
            ]
        }
    }


def generate_group_definition_layer(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate group definition layer - prepopulated access groups per table.

    Groups are defined at code generation time and inserted into the auth database
    via auth-schema.sql. No runtime API exists to create or delete groups.
    Admin/admin-group users can only grant or revoke membership.

    Args:
        db_def: Database definition

    Returns:
        Group definition layer dictionary
    """
    table_access_groups = []

    for table in db_def.tables:
        table_name = table.name
        entity_name = to_pascal_case(table_name)

        # TABLE_USER group: read-only + export
        table_access_groups.append({
            "groupName": f"{entity_name} Users",
            "description": f"User-level access to {table_name} table",
            "tableName": table_name,
            "entityName": entity_name,
            "groupType": "TABLE_USER",
            "accessLevel": "USER",
            "permissions": {
                "allowRead": True,
                "allowCreate": False,
                "allowUpdate": False,
                "allowDelete": False,
                "allowGrantAccess": False,
                "allowExport": True,
                "allowShare": False,
                "allowAudit": False
            }
        })

        # TABLE_ADMIN group: full CRUD
        table_access_groups.append({
            "groupName": f"{entity_name} Admins",
            "description": f"Admin-level access to {table_name} table",
            "tableName": table_name,
            "entityName": entity_name,
            "groupType": "TABLE_ADMIN",
            "accessLevel": "ADMIN",
            "permissions": {
                "allowRead": True,
                "allowCreate": True,
                "allowUpdate": True,
                "allowDelete": True,
                "allowGrantAccess": True,
                "allowExport": True,
                "allowShare": True,
                "allowAudit": True
            }
        })

    return {
        "layerType": "group_definition",
        "description": "Prepopulated access groups - no runtime group creation API. "
                       "Groups are inserted into auth database via auth-schema.sql. "
                       "Admin users can only grant/revoke membership at runtime.",
        "version": "1.0",
        "groupManagement": {
            "allowRuntimeCreation": False,
            "allowRuntimeDeletion": False,
            "adminCanGrantMembership": True,
            "adminCanRevokeMembership": True,
            "adminGroupName": "Administrators"
        },
        "ownerEnrollmentDefaults": {
            "ownershipCheck": "CREATOR_RECORDS",
            "maxRecordsPerUser": None,
            "allowEnroll": False,
            "allowUnenroll": False
        },
        "systemGroups": [
            {
                "groupName": "Super Administrators",
                "description": "Full system access - bypasses all authorization checks",
                "isSuperGroup": True,
                "isDefaultGroup": False,
                "autoAssignToNewUsers": False
            },
            {
                "groupName": "Administrators",
                "description": "Can grant/revoke group membership",
                "isSuperGroup": False,
                "isDefaultGroup": False,
                "autoAssignToNewUsers": False
            },
            {
                "groupName": "Standard Users",
                "description": "Default group for new users",
                "isSuperGroup": False,
                "isDefaultGroup": True,
                "autoAssignToNewUsers": True
            }
        ],
        "tableAccessGroups": table_access_groups,
        "queryAccessGroups": [],
        "queryAccessGroupExample": {
            "_comment": "Add query access groups here. Example structure:",
            "groupName": "Active Projects View",
            "description": "Shared view of active projects",
            "rootTable": "projects",
            "groupType": "QUERY_SPECIFIC",
            "scopeMode": "SPECIFIC_RECORDS",
            "ownerRecordEnrollment": {
                "allowEnroll": True,
                "allowUnenroll": True,
                "ownershipCheck": "CREATOR_RECORDS",
                "maxRecordsPerUser": None
            },
            "queryDefinition": {
                "table": "projects",
                "conditions": [
                    {"field": "status", "operator": "EQUALS", "value": "active"}
                ],
                "logic": "AND"
            }
        }
    }


def generate_authorization_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate authorization layer definition aligned with existing auth schema.

    Note: User groups and group management have been moved to group_definition_layer.
    This layer now only contains access control model configuration, document group types,
    entity access control settings, and permission/denial handling.

    Args:
        db_def: Database definition

    Returns:
        Authorization layer definition dictionary
    """
    # Generate entity access control configurations
    entity_access_controls = []
    for table in db_def.tables:
        entity_name = to_pascal_case(table.name)
        entity_access_controls.append({
            "entityName": entity_name,
            "tableName": table.name,
            "isRootEntity": True,
            "enableAccessControl": True,
            "checkOnCreate": True,
            "checkOnRead": True,
            "checkOnUpdate": True,
            "checkOnDelete": True,
            "customRules": []
        })

    return {
        "layerType": "authorization",
        "description": "Authorization configuration - document-based access control aligned with existing auth schema. "
                       "User groups and membership settings are defined in group_definition_layer.json.",
        "enabled": True,
        "accessControlModel": "document-based",
        "accessControls": [
            {
                "name": "READ",
                "description": "View document content",
                "enabled": True
            },
            {
                "name": "CREATE",
                "description": "Create new documents",
                "enabled": True
            },
            {
                "name": "UPDATE",
                "description": "Modify existing documents",
                "enabled": True
            },
            {
                "name": "DELETE",
                "description": "Remove documents",
                "enabled": True
            },
            {
                "name": "GRANT_ACCESS",
                "description": "Grant access to other users",
                "enabled": True
            },
            {
                "name": "EXPORT",
                "description": "Export document data",
                "enabled": True
            },
            {
                "name": "SHARE",
                "description": "Share documents temporarily",
                "enabled": True
            },
            {
                "name": "AUDIT",
                "description": "View access logs",
                "enabled": True
            }
        ],
        "documentGroupTypes": [
            {
                "name": "SINGLE_RECORD",
                "description": "Single record in a table",
                "enabled": True,
                "requiresTableName": True,
                "requiresRecordIds": True,
                "supportsQuery": False
            },
            {
                "name": "MULTIPLE_RECORDS",
                "description": "Multiple specific records in a table",
                "enabled": True,
                "requiresTableName": True,
                "requiresRecordIds": True,
                "supportsQuery": False,
                "recordIdsFormat": "JSON array"
            },
            {
                "name": "ENTIRE_TABLE",
                "description": "All records in a table",
                "enabled": True,
                "requiresTableName": True,
                "requiresRecordIds": False,
                "supportsQuery": False
            },
            {
                "name": "MULTIPLE_TABLES",
                "description": "All records in multiple tables",
                "enabled": True,
                "requiresTableName": True,
                "requiresRecordIds": False,
                "supportsQuery": False,
                "tableNameFormat": "Comma-separated list"
            },
            {
                "name": "CUSTOM_QUERY",
                "description": "Records matching a predefined query (requires explicit record IDs)",
                "enabled": True,
                "requiresTableName": True,
                "requiresRecordIds": True,
                "supportsQuery": True,
                "queryFormat": "JSON query definition"
            },
            {
                "name": "CUSTOM_QUERY_ALL",
                "description": "All records matching a predefined query (ignores record IDs)",
                "enabled": True,
                "requiresTableName": True,
                "requiresRecordIds": False,
                "supportsQuery": True,
                "queryFormat": "JSON query definition"
            }
        ],
        "superUserSettings": {
            "enabled": True,
            "bypassAllChecks": True,
            "requireJustificationForDelete": True,
            "justificationMinLength": 10,
            "logAllActions": True
        },
        "entityAccessControl": entity_access_controls,
        "permissionSettings": {
            "allowUserPermissions": True,
            "allowGroupPermissions": True,
            "requireExpirationDate": False,
            "unionPermissions": True,
            "mostPermissiveWins": True
        },
        "queryDefinitionFormat": {
            "description": "JSON format for CUSTOM_QUERY and CUSTOM_QUERY_ALL types",
            "example": {
                "table": "users",
                "conditions": [
                    {
                        "field": "status",
                        "operator": "EQUALS",
                        "value": "active"
                    },
                    {
                        "field": "department",
                        "operator": "IN",
                        "value": ["sales", "marketing"]
                    }
                ],
                "logic": "AND"
            },
            "supportedOperators": [
                "EQUALS",
                "NOT_EQUALS",
                "GREATER_THAN",
                "LESS_THAN",
                "GREATER_THAN_OR_EQUAL",
                "LESS_THAN_OR_EQUAL",
                "LIKE",
                "IN",
                "NOT_IN"
            ],
            "supportedLogic": ["AND", "OR"]
        },
        "accessControlChecks": {
            "checkOnCreate": True,
            "checkOnRead": True,
            "checkOnUpdate": True,
            "checkOnDelete": True,
            "checkOnList": True,
            "createUsesRecordIdZero": True
        },
        "denialHandling": {
            "throwExceptionOnDenial": True,
            "exceptionType": "RuntimeException",
            "exceptionMessage": "Access denied",
            "logDenials": True,
            "includeDenialReason": True
        }
    }


def generate_custom_queries_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate custom queries layer definition with examples.

    Args:
        db_def: Database definition

    Returns:
        Custom queries layer definition dictionary
    """
    # Generate example queries for first few entities
    example_queries = []
    for table in db_def.tables[:3]:  # First 3 as examples
        entity_name = to_pascal_case(table.name)

        # Find a status or active field if exists
        status_field = None
        for col in table.columns:
            if 'status' in col.name.lower() or 'active' in col.name.lower():
                status_field = col.name
                break

        if status_field:
            example_queries.append({
                "queryName": f"Active{entity_name}s",
                "description": f"All active {entity_name.lower()} records",
                "table": table.name,
                "conditions": [
                    {
                        "field": status_field,
                        "operator": "EQUALS",
                        "value": "active"
                    }
                ],
                "logic": "AND"
            })

    return {
        "layerType": "customQueries",
        "description": "Custom query templates for authorization - used with CUSTOM_QUERY and CUSTOM_QUERY_ALL document group types",
        "queries": example_queries,
        "queryFormat": {
            "description": "JSON format for defining custom queries",
            "structure": {
                "queryName": "Unique identifier for the query",
                "description": "Human-readable description",
                "table": "Target table name",
                "conditions": [
                    {
                        "field": "Column name",
                        "operator": "Comparison operator",
                        "value": "Value to compare against"
                    }
                ],
                "logic": "AND or OR - how to combine conditions"
            },
            "supportedOperators": [
                "EQUALS",
                "NOT_EQUALS",
                "GREATER_THAN",
                "LESS_THAN",
                "GREATER_THAN_OR_EQUAL",
                "LESS_THAN_OR_EQUAL",
                "LIKE",
                "IN",
                "NOT_IN"
            ],
            "supportedLogic": ["AND", "OR"]
        },
        "examples": [
            {
                "queryName": "ActiveUsers",
                "description": "All active user accounts",
                "table": "users",
                "conditions": [
                    {
                        "field": "status",
                        "operator": "EQUALS",
                        "value": "active"
                    }
                ],
                "logic": "AND"
            },
            {
                "queryName": "SalesDepartment",
                "description": "All users in sales or marketing departments",
                "table": "users",
                "conditions": [
                    {
                        "field": "department",
                        "operator": "IN",
                        "value": ["sales", "marketing"]
                    }
                ],
                "logic": "AND"
            },
            {
                "queryName": "RecentOrders",
                "description": "Orders from the last 30 days",
                "table": "orders",
                "conditions": [
                    {
                        "field": "created_date",
                        "operator": "GREATER_THAN",
                        "value": "NOW() - INTERVAL 30 DAY"
                    }
                ],
                "logic": "AND"
            }
        ]
    }








def generate_query_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate query layer definition from database definition.
    
    Creates empty query definitions for each entity that users can populate.
    """
    queries_by_entity = {}
    
    # Transform all entities first
    entities = []
    for table in db_def.tables:
        entity_obj = EntityTransformer.transform(table, db_def.projectMetadata.groupId)
        entities.append(entity_obj)
    
    # Use DefaultQueryTransformer to generate intelligent default queries
    default_query_transformer = DefaultQueryTransformer(
        db_def.tables, 
        entities, 
        db_def.projectMetadata.groupId
    )
    query_layers = default_query_transformer.transform()
    
    # Convert to dictionary format with serializable queries
    for query_layer in query_layers:
        # Convert CustomQuery objects to dictionaries
        serializable_queries = []
        for query in query_layer.queries:
            query_dict = {
                "name": query.name,
                "description": query.description,
                "returnType": query.returnType,
                "select": query.select,
                "from": query.from_,
                "joins": [
                    {
                        "type": join.type,
                        "table": join.table,
                        "alias": join.alias,
                        "on": join.on
                    }
                    for join in query.joins
                ],
                "where": query.where,
                "groupBy": query.groupBy,
                "having": query.having,
                "orderBy": query.orderBy,
                "pagination": query.pagination,
                "parameters": [
                    {
                        "name": param.name,
                        "type": param.type,
                        "required": param.required,
                        "defaultValue": param.defaultValue
                    }
                    for param in query.parameters
                ],
                "authorization": query.authorization
            }
            serializable_queries.append(query_dict)
        
        queries_by_entity[query_layer.entityName] = serializable_queries
    
    return {
        "layerType": "query",
        "description": "Custom query definitions - define R2DBC DatabaseClient queries with joins, aggregations, and filters. Default queries are auto-generated based on table relationships.",
        "version": "2.4.0",
        "queries": queries_by_entity,
        "queryStructure": {
            "name": "Query method name (camelCase)",
            "description": "Human-readable description",
            "returnType": "DTO class name for results",
            "select": ["List of SELECT fields (e.g., 'u.id', 'u.username', 'COUNT(r.id) as role_count')"],
            "from": "FROM clause with alias (e.g., 'users u')",
            "joins": [
                {
                    "type": "INNER|LEFT|RIGHT|FULL",
                    "table": "Table name",
                    "alias": "Optional table alias",
                    "on": "Join condition (e.g., 'u.id = ur.user_id')"
                }
            ],
            "where": ["List of WHERE conditions (e.g., 'u.active = :active')"],
            "groupBy": ["List of GROUP BY fields"],
            "having": ["List of HAVING conditions"],
            "orderBy": ["List of ORDER BY clauses (e.g., 'u.username ASC')"],
            "pagination": "true|false - Enable pagination support",
            "parameters": [
                {
                    "name": "Parameter name",
                    "type": "Java type (String, Integer, Boolean, LocalDateTime, etc.)",
                    "required": "true|false",
                    "defaultValue": "Optional default value"
                }
            ],
            "authorization": {
                "enabled": "true|false - Check document access",
                "documentField": "Field name containing document ID for authorization check"
            }
        },
        "examples": [
            {
                "name": "findActiveUsersWithRoles",
                "description": "Find active users with their roles",
                "returnType": "UserWithRolesDTO",
                "select": ["u.id", "u.username", "u.email", "r.role_name"],
                "from": "users u",
                "joins": [
                    {
                        "type": "INNER",
                        "table": "user_roles",
                        "alias": "ur",
                        "on": "u.id = ur.user_id"
                    },
                    {
                        "type": "LEFT",
                        "table": "roles",
                        "alias": "r",
                        "on": "ur.role_id = r.id"
                    }
                ],
                "where": ["u.active = :active", "u.created_date > :fromDate"],
                "groupBy": ["u.id", "u.username"],
                "having": ["COUNT(r.id) > :minRoles"],
                "orderBy": ["u.username ASC"],
                "pagination": True,
                "parameters": [
                    {"name": "active", "type": "Boolean", "required": True},
                    {"name": "fromDate", "type": "LocalDateTime", "required": False},
                    {"name": "minRoles", "type": "Integer", "required": False, "defaultValue": "1"}
                ],
                "authorization": {
                    "enabled": True,
                    "documentField": "id"
                }
            }
        ],
        "notes": [
            "All queries are generated as R2DBC DatabaseClient parameterized queries",
            "No dynamic SQL generation at runtime - all queries are pre-built",
            "Authorization checks are applied at the service layer if enabled",
            "Pagination adds LIMIT and OFFSET parameters automatically",
            "Query results are mapped to DTOs specified in returnType"
        ]
    }


def generate_filter_layer_definition(db_def: DatabaseDefinition) -> Dict[str, Any]:
    """Generate filter layer definition from database definition.
    
    Creates filter definitions for each entity based on their fields.
    """
    filters_by_entity = {}
    
    for table in db_def.tables:
        # Transform to entity first
        entity_obj = EntityTransformer.transform(table, db_def.projectMetadata.groupId)
        
        # Use transformer to get filter layer with defaults
        filter_layers = FilterTransformer.transform([entity_obj], db_def.projectMetadata.groupId)
        
        # Add to dictionary
        for filter_layer in filter_layers:
            filters_by_entity[filter_layer.entityName] = {
                "fields": [
                    {
                        "name": field.name,
                        "type": field.type,
                        "operators": field.operators
                    }
                    for field in filter_layer.fields
                ]
            }
    
    return {
        "layerType": "filter",
        "description": "Filter definitions - entity-specific filter fields and operators for custom queries",
        "version": "2.4.0",
        "filters": filters_by_entity,
        "filterStructure": {
            "fields": [
                {
                    "name": "Field name (camelCase)",
                    "type": "Java type (String, Integer, Boolean, LocalDateTime, etc.)",
                    "operators": ["List of supported operators"]
                }
            ]
        },
        "supportedOperators": {
            "equals": "Exact match (field = value)",
            "contains": "String contains (field LIKE '%value%')",
            "startsWith": "String starts with (field LIKE 'value%')",
            "endsWith": "String ends with (field LIKE '%value')",
            "greaterThan": "Greater than (field > value)",
            "lessThan": "Less than (field < value)",
            "between": "Between two values (field BETWEEN value1 AND value2)",
            "in": "In list (field IN (value1, value2, ...))"
        },
        "operatorsByType": {
            "String": ["equals", "contains", "startsWith", "endsWith", "in"],
            "Integer/Long/Short/Byte": ["equals", "greaterThan", "lessThan", "between", "in"],
            "BigDecimal/Float/Double": ["equals", "greaterThan", "lessThan", "between", "in"],
            "Boolean": ["equals"],
            "LocalDate/LocalDateTime/LocalTime": ["equals", "greaterThan", "lessThan", "between"]
        },
        "notes": [
            "Filters are entity-specific and not reusable across entities",
            "Filter DTOs are auto-generated based on field definitions",
            "Each operator generates corresponding DTO fields (e.g., 'usernameContains' for contains operator)",
            "Filters are applied in custom queries defined in query_layer.json"
        ]
    }
