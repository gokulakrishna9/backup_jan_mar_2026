"""Main entry point for Spring WebFlux Application Writer v2."""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from models.database_definition import DatabaseDefinition
from transformers import (
    EntityTransformer, DTOTransformer, RepositoryTransformer,
    ServiceTransformer, ControllerTransformer,
    SecurityTransformer, JWTTransformer, ConfigTransformer,
    POMTransformer
)
from generators import (
    EntityGenerator, DTOGenerator, RepositoryGenerator,
    ServiceGenerator, ControllerGenerator,
    SecurityGenerator, JWTGenerator, ConfigGenerator,
    POMGenerator, TestDataGenerator, AuthSchemaGenerator,
    AuthEntityGenerator, AuthRepositoryGenerator, SetupGenerator,
    AuthServiceGenerator, AuthorizationServiceGenerator, AuditLoggingGenerator,
    AdminUIGenerator, OAuth2Generator, ExceptionGenerator,
    ActivityTrackingGenerator, ActivityTrackingSchemaGenerator
)
from generators.permissions_generator import PermissionsGenerator
from utils.file_writer import create_directory_structure, write_file, write_binary_file


def generate_from_transformers(db_def: DatabaseDefinition, dirs: dict, package_name: str, all_entities: list):
    """Generate code using transformers (legacy mode)."""
    for table in db_def.tables:
        print(f"\n>> Processing table: {table.name}")
        
        # 1. Generate Entity
        entity = EntityTransformer.transform(table, package_name)
        all_entities.append(entity)
        entity_code = EntityGenerator.generate(entity)
        entity_path = dirs['entity'] / f"{entity.className}.java"
        write_file(entity_path, entity_code)
        
        # 2. Generate DTOs
        for dto_type in ['Input', 'Output', 'Filter']:
            dto = DTOTransformer.transform(entity, dto_type)
            dto_code = DTOGenerator.generate(dto)
            dto_path = dirs['dto'] / f"{dto.className}.java"
            write_file(dto_path, dto_code)
        
        # 3. Generate Repository
        repository = RepositoryTransformer.transform(entity)
        repo_code = RepositoryGenerator.generate(repository)
        repo_path = dirs['repository'] / f"{repository.className}.java"
        write_file(repo_path, repo_code)
        
        # 4. Generate Service
        service = ServiceTransformer.transform(entity)
        service_code = ServiceGenerator.generate(service, entity)
        service_path = dirs['service'] / f"{service.className}.java"
        write_file(service_path, service_code)
        
        # 5. Generate Controller
        controller = ControllerTransformer.transform(entity)
        controller_code = ControllerGenerator.generate(controller, has_authorization=service.hasAuthorization)
        controller_path = dirs['controller'] / f"{controller.className}.java"
        write_file(controller_path, controller_code)


def generate_from_layer_definitions(db_def: DatabaseDefinition, layer_definitions: dict, dirs: dict, package_name: str, all_entities: list):
    """Generate code using layer definition files (v2.3+)."""
    entity_defs = layer_definitions['entity_layer']['entities']
    repo_defs = layer_definitions['repository_layer']['repositories']
    service_defs = layer_definitions['service_layer']['services']
    controller_defs = layer_definitions['controller_layer']['controllers']
    dto_defs = layer_definitions['dto_layer']['dtos']
    
    # Create lookup dictionaries by entity name
    repo_lookup = {r['entityName']: r for r in repo_defs}
    service_lookup = {s['entityName']: s for s in service_defs}
    controller_lookup = {c['entityName']: c for c in controller_defs}
    
    # Group DTOs by entity name
    dto_lookup = {}
    for dto_def in dto_defs:
        entity_name = dto_def['entityName']
        if entity_name not in dto_lookup:
            dto_lookup[entity_name] = {}
        dto_lookup[entity_name][dto_def['dtoType']] = dto_def
    
    # Generate code for each entity
    for entity_def in entity_defs:
        entity_name = entity_def['className']
        print(f"\n>> Processing entity: {entity_name}")
        
        # 1. Generate Entity from definition
        # Convert definition dict to EntityLayerObject
        from models.layer_objects import EntityLayerObject, Field
        
        fields = [Field(**field_def) for field_def in entity_def['fields']]
        entity = EntityLayerObject(
            tableName=entity_def['tableName'],
            className=entity_def['className'],
            packageName=entity_def['packageName'],
            fields=fields,
            isRootEntity=entity_def['isRootEntity'],
            parentEntity=entity_def.get('parentEntity'),
            hasPublicFlag=entity_def['hasPublicFlag'],
            hasAuditFields=entity_def.get('hasAuditFields', True),
            hasSoftDelete=entity_def.get('hasSoftDelete', True),
            relationships=entity_def.get('relationships', [])
        )
        all_entities.append(entity)
        
        entity_code = EntityGenerator.generate(entity)
        entity_path = dirs['entity'] / f"{entity.className}.java"
        write_file(entity_path, entity_code)
        
        # 2. Generate DTOs from definitions
        if entity_name in dto_lookup:
            for dto_type in ['Input', 'Output', 'Filter']:
                if dto_type in dto_lookup[entity_name]:
                    dto_def = dto_lookup[entity_name][dto_type]
                    
                    # Convert definition dict to DTOLayerObject
                    from models.layer_objects import DTOLayerObject
                    
                    # Add columnName to DTO fields (same as fieldName for DTOs)
                    dto_fields = []
                    for field_def in dto_def['fields']:
                        if 'columnName' not in field_def:
                            field_def['columnName'] = field_def['fieldName']
                        dto_fields.append(Field(**field_def))
                    
                    dto = DTOLayerObject(
                        entityName=dto_def['entityName'],
                        className=dto_def['className'],
                        packageName=dto_def['packageName'],
                        fields=dto_fields,
                        dtoType=dto_def['dtoType'],
                        isRootEntity=entity_def['isRootEntity'],
                        fieldConfigs=dto_def.get('fields', []),  # Use fields as fieldConfigs
                        customValidators=dto_def.get('customValidators', []),
                        excludeSensitiveFields=dto_def.get('excludeSensitiveFields', []),
                        includeRelationships=dto_def.get('includeRelationships', False)
                    )
                    
                    dto_code = DTOGenerator.generate(dto)
                    dto_path = dirs['dto'] / f"{dto.className}.java"
                    write_file(dto_path, dto_code)
        
        # 3. Generate Repository from definition
        if entity_name in repo_lookup:
            repo_def = repo_lookup[entity_name]
            
            # Convert definition dict to RepositoryLayerObject
            from models.layer_objects import RepositoryLayerObject
            
            repository = RepositoryLayerObject(
                entityName=repo_def['entityName'],
                className=repo_def['className'],
                packageName=repo_def['packageName'],
                idType=repo_def['idType'],
                hasCustomQueries=repo_def.get('hasCustomQueries', False),
                customQueries=repo_def.get('customQueries', []),
                hasSoftDelete=repo_def.get('hasSoftDelete', False),
                hasAuthorization=repo_def.get('hasAuthorization', False),
                singleRecordPerUser=repo_def.get('singleRecordPerUser', False),
                tableName=entity_def.get('tableName'),
                idColumn=next((f['columnName'] for f in entity_def.get('fields', []) if f.get('isPrimaryKey')), None),
            )
            
            repo_code = RepositoryGenerator.generate(repository)
            repo_path = dirs['repository'] / f"{repository.className}.java"
            write_file(repo_path, repo_code)
        
        # 4. Generate Service from definition
        if entity_name in service_lookup:
            service_def = service_lookup[entity_name]
            
            # Convert definition dict to ServiceLayerObject
            from models.layer_objects import ServiceLayerObject
            
            service = ServiceLayerObject(
                entityName=service_def['entityName'],
                className=service_def['className'],
                packageName=service_def['packageName'],
                repositoryName=service_def['repositoryName'],
                isRootEntity=service_def['isRootEntity'],
                hasAuthorization=service_def.get('hasAuthorization', False),
                singleRecordPerUser=service_def.get('singleRecordPerUser', False)
            )
            
            service_code = ServiceGenerator.generate(service, entity)
            service_path = dirs['service'] / f"{service.className}.java"
            write_file(service_path, service_code)
        
        # 5. Generate Controller from definition
        if entity_name in controller_lookup:
            controller_def = controller_lookup[entity_name]
            
            # Convert definition dict to ControllerLayerObject
            from models.layer_objects import ControllerLayerObject
            
            controller = ControllerLayerObject(
                entityName=controller_def['entityName'],
                className=controller_def['className'],
                packageName=controller_def['packageName'],
                serviceName=controller_def['serviceName'],
                basePath=controller_def['basePath'],
                isRootEntity=controller_def['isRootEntity'],
                endpoints=controller_def.get('endpoints', {}),
                customEndpoints=controller_def.get('customEndpoints', []),
                corsConfig=controller_def.get('corsConfig', {}),
                singleRecordPerUser=controller_def.get('singleRecordPerUser', False)
            )
            
            controller_code = ControllerGenerator.generate(controller, has_authorization=service_def.get('hasAuthorization', False))
            controller_path = dirs['controller'] / f"{controller.className}.java"
            write_file(controller_path, controller_code)


def load_database_definition(input_file: str) -> DatabaseDefinition:
    """Load and parse database definition from JSON file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return DatabaseDefinition(**data)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to parse database definition: {e}")
        sys.exit(1)


def generate_application(db_def: DatabaseDefinition, output_dir: str):
    """Load and parse database definition from JSON file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return DatabaseDefinition(**data)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to parse database definition: {e}")
        sys.exit(1)


def _load_layer_definitions_direct(definitions_dir: str):
    """Load layer definitions directly from a directory (no /application_definitions/ subdirectory)."""
    import json
    from pathlib import Path
    defs_path = Path(definitions_dir)
    if not defs_path.exists():
        return None
    layer_files = {
        'entity_layer': 'webflux_entity_layer.json',
        'repository_layer': 'webflux_repository_layer.json',
        'service_layer': 'webflux_service_layer.json',
        'controller_layer': 'webflux_controller_layer.json',
        'dto_layer': 'webflux_dto_layer.json',
    }
    result = {}
    for key, filename in layer_files.items():
        fpath = defs_path / filename
        if not fpath.exists():
            return None
        with open(fpath, 'r', encoding='utf-8') as f:
            result[key] = json.load(f)
    return result


def generate_application(db_def: DatabaseDefinition, output_dir: str, definitions_dir: str = None):
    """Generate complete Spring WebFlux application.
    
    Code is written to output_dir/webflux_app/ while application_definitions/
    are read from definitions_dir (if provided) or output_dir/application_definitions/.
    """
    import os
    import shutil
    code_dir = os.path.join(output_dir, 'webflux_app')
    
    print(f"\n>> Generating Spring WebFlux Application: {db_def.projectMetadata.name}")
    print(f">> Output directory: {code_dir}\n")
    
    # Clean generated Java source to remove stale files from previous generations
    src_main_java = os.path.join(code_dir, 'src', 'main', 'java')
    if os.path.exists(src_main_java):
        print(f">> Cleaning previous generated source: {src_main_java}")
        shutil.rmtree(src_main_java)
    
    # Create directory structure inside webflux_app/
    package_name = db_def.projectMetadata.groupId
    dirs = create_directory_structure(code_dir, package_name)
    
    # Note: application_definition.json should already exist from Phase 1
    # We don't overwrite it here to preserve any manual edits
    
    # Try to load layer definitions (v2.3+)
    # If definitions_dir is provided, look there directly; otherwise fall back to output_dir
    from utils.definition_splitter import load_layer_definitions_if_exist
    layer_definitions = None
    if definitions_dir:
        # definitions_dir points directly to the app definitions folder
        # (e.g., application_definitions/job_portal)
        layer_definitions = _load_layer_definitions_direct(definitions_dir)
    if not layer_definitions:
        layer_definitions = load_layer_definitions_if_exist(output_dir)
    
    if layer_definitions:
        print(f">> Using layer definition files (customizable configuration)")
        print(f"   - entity_layer.json")
        print(f"   - repository_layer.json")
        print(f"   - service_layer.json")
        print(f"   - controller_layer.json")
        print(f"   - dto_layer.json\n")
    else:
        print(f">> Using transformer-based generation (legacy mode)\n")
    
    # Store all entity objects for authorization service
    all_entities = []
    
    # Generate code for each table
    if layer_definitions:
        # NEW: Use layer definitions
        generate_from_layer_definitions(db_def, layer_definitions, dirs, package_name, all_entities)
    else:
        # LEGACY: Use transformers
        generate_from_transformers(db_def, dirs, package_name, all_entities)
        
    
    print(f"\n>> Generating authentication/authorization entities and repositories...")
    
    # Generate Auth Entities
    auth_entities = [
        # Retained entities
        ('SystemConfig', AuthEntityGenerator.generate_system_config),
        ('AuthUser', AuthEntityGenerator.generate_auth_user),
        ('AccessAuditLog', AuthEntityGenerator.generate_access_audit_log),
        # New simplified authorization entities
        ('UserRole', AuthEntityGenerator.generate_user_role),
        ('RecordOwner', AuthEntityGenerator.generate_record_owner),
        ('QueryGroup', AuthEntityGenerator.generate_query_group),
        ('QueryGroupQuery', AuthEntityGenerator.generate_query_group_query),
        ('QueryGroupMember', AuthEntityGenerator.generate_query_group_member),
        ('QueryGroupRecord', AuthEntityGenerator.generate_query_group_record),
    ]
    
    for entity_name, generator_func in auth_entities:
        entity_code = generator_func(package_name)
        entity_path = dirs['entity'] / f"{entity_name}.java"
        write_file(entity_path, entity_code)
    
    # Generate Auth Repositories
    auth_repositories = [
        # Retained repositories
        ('SystemConfigRepository', AuthRepositoryGenerator.generate_system_config_repository),
        ('AuthUserRepository', AuthRepositoryGenerator.generate_auth_user_repository),
        ('AccessAuditLogRepository', AuthRepositoryGenerator.generate_access_audit_log_repository),
        # New simplified authorization repositories
        ('UserRoleRepository', AuthRepositoryGenerator.generate_user_role_repository),
        ('RecordOwnerRepository', AuthRepositoryGenerator.generate_record_owner_repository),
        ('QueryGroupRepository', AuthRepositoryGenerator.generate_query_group_repository),
        ('QueryGroupQueryRepository', AuthRepositoryGenerator.generate_query_group_query_repository),
        ('QueryGroupMemberRepository', AuthRepositoryGenerator.generate_query_group_member_repository),
        ('QueryGroupRecordRepository', AuthRepositoryGenerator.generate_query_group_record_repository),
    ]
    
    for repo_name, generator_func in auth_repositories:
        repo_code = generator_func(package_name)
        repo_path = dirs['repository'] / f"{repo_name}.java"
        write_file(repo_path, repo_code)
    
    print(f"\n>> Generating authorization service components...")
    
    # Generate RoleAuthorizationService
    role_auth_service_code = AuthorizationServiceGenerator.generate_role_authorization_service(package_name)
    role_auth_service_path = dirs['service'] / "RoleAuthorizationService.java"
    write_file(role_auth_service_path, role_auth_service_code)
    
    # Generate AuthorizationWebFilter
    auth_web_filter_code = AuthorizationServiceGenerator.generate_authorization_web_filter(package_name)
    auth_web_filter_path = dirs['security'] / "AuthorizationWebFilter.java"
    write_file(auth_web_filter_path, auth_web_filter_code)
    
    # Generate @EntityTable annotation
    entity_table_annotation_code = AuthorizationServiceGenerator.generate_entity_table_annotation(package_name)
    entity_table_annotation_path = dirs['security'] / "EntityTable.java"
    write_file(entity_table_annotation_path, entity_table_annotation_code)
    
    # Generate @TableAccess annotation
    table_access_annotation_code = AuthorizationServiceGenerator.generate_table_access_annotation(package_name)
    table_access_annotation_path = dirs['security'] / "TableAccess.java"
    write_file(table_access_annotation_path, table_access_annotation_code)
    
    # Generate @QueryAccess annotation
    query_access_annotation_code = AuthorizationServiceGenerator.generate_query_access_annotation(package_name)
    query_access_annotation_path = dirs['security'] / "QueryAccess.java"
    write_file(query_access_annotation_path, query_access_annotation_code)
    
    # Generate AuthorizationAspect (AOP-based authorization — replaces WebFilter approach)
    auth_aspect_code = AuthorizationServiceGenerator.generate_authorization_aspect(package_name)
    auth_aspect_path = dirs['security'] / "AuthorizationAspect.java"
    write_file(auth_aspect_path, auth_aspect_code)
    
    print(f"\n>> Generating audit logging components...")
    
    # Generate AuditLoggingService
    audit_logging_service_code = AuditLoggingGenerator.generate_audit_logging_service(package_name)
    audit_logging_service_path = dirs['service'] / "AuditLoggingService.java"
    write_file(audit_logging_service_path, audit_logging_service_code)
    
    # Generate AuditController
    audit_controller_code = AuditLoggingGenerator.generate_audit_controller(package_name)
    audit_controller_path = dirs['controller'] / "AuditController.java"
    write_file(audit_controller_path, audit_controller_code)
    
    print(f"\n>> Generating admin UI components...")
    
    # Generate AdminService
    admin_service_code = AdminUIGenerator.generate_admin_service(package_name)
    admin_service_path = dirs['service'] / "AdminService.java"
    write_file(admin_service_path, admin_service_code)
    
    # Generate AdminController
    admin_controller_code = AdminUIGenerator.generate_admin_controller(package_name)
    admin_controller_path = dirs['controller'] / "AdminController.java"
    write_file(admin_controller_path, admin_controller_code)
    
    # Generate Admin HTML Templates
    dashboard_html = AdminUIGenerator.generate_dashboard_html()
    dashboard_path = dirs['templates_admin'] / "dashboard.html"
    write_file(dashboard_path, dashboard_html)
    
    groups_html = AdminUIGenerator.generate_groups_html()
    groups_path = dirs['templates_admin'] / "groups.html"
    write_file(groups_path, groups_html)
    
    group_form_html = AdminUIGenerator.generate_group_form_html()
    group_form_path = dirs['templates_admin'] / "group-form.html"
    write_file(group_form_path, group_form_html)
    
    users_html = AdminUIGenerator.generate_users_html()
    users_path = dirs['templates_admin'] / "users.html"
    write_file(users_path, users_html)
    
    user_detail_html = AdminUIGenerator.generate_user_detail_html()
    user_detail_path = dirs['templates_admin'] / "user-detail.html"
    write_file(user_detail_path, user_detail_html)
    
    document_groups_html = AdminUIGenerator.generate_document_groups_html()
    document_groups_path = dirs['templates_admin'] / "document-groups.html"
    write_file(document_groups_path, document_groups_html)
    
    document_group_form_html = AdminUIGenerator.generate_document_group_form_html()
    document_group_form_path = dirs['templates_admin'] / "document-group-form.html"
    write_file(document_group_form_path, document_group_form_html)
    
    document_group_detail_html = AdminUIGenerator.generate_document_group_detail_html()
    document_group_detail_path = dirs['templates_admin'] / "document-group-detail.html"
    write_file(document_group_detail_path, document_group_detail_html)
    
    print(f"\n>> Generating OAuth2 and SAML authentication components...")
    
    # Generate OAuth2 Entities
    oauth2_provider_code = OAuth2Generator.generate_oauth2_provider_entity(package_name)
    oauth2_provider_path = dirs['entity'] / "OAuth2Provider.java"
    write_file(oauth2_provider_path, oauth2_provider_code)
    
    oauth2_linked_account_code = OAuth2Generator.generate_oauth2_linked_account_entity(package_name)
    oauth2_linked_account_path = dirs['entity'] / "OAuth2LinkedAccount.java"
    write_file(oauth2_linked_account_path, oauth2_linked_account_code)
    
    # Generate OAuth2 Repositories
    oauth2_provider_repo_code = OAuth2Generator.generate_oauth2_provider_repository(package_name)
    oauth2_provider_repo_path = dirs['repository'] / "OAuth2ProviderRepository.java"
    write_file(oauth2_provider_repo_path, oauth2_provider_repo_code)
    
    oauth2_linked_account_repo_code = OAuth2Generator.generate_oauth2_linked_account_repository(package_name)
    oauth2_linked_account_repo_path = dirs['repository'] / "OAuth2LinkedAccountRepository.java"
    write_file(oauth2_linked_account_repo_path, oauth2_linked_account_repo_code)
    
    # Generate OAuth2 Service
    oauth2_service_code = OAuth2Generator.generate_oauth2_service(package_name)
    oauth2_service_path = dirs['service'] / "OAuth2Service.java"
    write_file(oauth2_service_path, oauth2_service_code)
    
    # Generate OAuth2 Controller
    oauth2_controller_code = OAuth2Generator.generate_oauth2_controller(package_name)
    oauth2_controller_path = dirs['controller'] / "OAuth2Controller.java"
    write_file(oauth2_controller_path, oauth2_controller_code)
    
    print(f"\n>> Generating exception handling components...")
    
    # Generate Exception Classes
    global_exception_handler_code = ExceptionGenerator.generate_global_exception_handler(package_name)
    global_exception_handler_path = dirs['exception'] / "GlobalExceptionHandler.java"
    write_file(global_exception_handler_path, global_exception_handler_code)
    
    error_response_code = ExceptionGenerator.generate_error_response(package_name)
    error_response_path = dirs['exception'] / "ErrorResponse.java"
    write_file(error_response_path, error_response_code)
    
    validation_error_response_code = ExceptionGenerator.generate_validation_error_response(package_name)
    validation_error_response_path = dirs['exception'] / "ValidationErrorResponse.java"
    write_file(validation_error_response_path, validation_error_response_code)
    
    entity_not_found_exception_code = ExceptionGenerator.generate_entity_not_found_exception(package_name)
    entity_not_found_exception_path = dirs['exception'] / "EntityNotFoundException.java"
    write_file(entity_not_found_exception_path, entity_not_found_exception_code)
    
    access_denied_exception_code = ExceptionGenerator.generate_access_denied_exception(package_name)
    access_denied_exception_path = dirs['exception'] / "AccessDeniedException.java"
    write_file(access_denied_exception_path, access_denied_exception_code)
    
    duplicate_entity_exception_code = ExceptionGenerator.generate_duplicate_entity_exception(package_name)
    duplicate_entity_exception_path = dirs['exception'] / "DuplicateEntityException.java"
    write_file(duplicate_entity_exception_path, duplicate_entity_exception_code)
    
    # Generate PageResponse DTO (shared pagination wrapper)
    page_response_code = ExceptionGenerator.generate_page_response(package_name)
    page_response_path = dirs['dto'] / "PageResponse.java"
    write_file(page_response_path, page_response_code)
    
    print(f"\n>> Generating activity tracking components...")
    
    # Generate Activity Tracking Entities
    crud_activity_log_code = ActivityTrackingGenerator.generate_crud_activity_log_entity(package_name)
    crud_activity_log_path = dirs['entity'] / "CrudActivityLog.java"
    write_file(crud_activity_log_path, crud_activity_log_code)
    
    deleted_record_code = ActivityTrackingGenerator.generate_deleted_record_entity(package_name)
    deleted_record_path = dirs['entity'] / "DeletedRecord.java"
    write_file(deleted_record_path, deleted_record_code)
    
    login_activity_log_code = ActivityTrackingGenerator.generate_login_activity_log_entity(package_name)
    login_activity_log_path = dirs['entity'] / "LoginActivityLog.java"
    write_file(login_activity_log_path, login_activity_log_code)
    
    grant_activity_log_code = ActivityTrackingGenerator.generate_grant_activity_log_entity(package_name)
    grant_activity_log_path = dirs['entity'] / "GrantActivityLog.java"
    write_file(grant_activity_log_path, grant_activity_log_code)
    
    # Generate Activity Tracking Repositories
    crud_activity_log_repo_code = ActivityTrackingGenerator.generate_crud_activity_log_repository(package_name)
    crud_activity_log_repo_path = dirs['repository'] / "CrudActivityLogRepository.java"
    write_file(crud_activity_log_repo_path, crud_activity_log_repo_code)
    
    deleted_record_repo_code = ActivityTrackingGenerator.generate_deleted_record_repository(package_name)
    deleted_record_repo_path = dirs['repository'] / "DeletedRecordRepository.java"
    write_file(deleted_record_repo_path, deleted_record_repo_code)
    
    login_activity_log_repo_code = ActivityTrackingGenerator.generate_login_activity_log_repository(package_name)
    login_activity_log_repo_path = dirs['repository'] / "LoginActivityLogRepository.java"
    write_file(login_activity_log_repo_path, login_activity_log_repo_code)
    
    grant_activity_log_repo_code = ActivityTrackingGenerator.generate_grant_activity_log_repository(package_name)
    grant_activity_log_repo_path = dirs['repository'] / "GrantActivityLogRepository.java"
    write_file(grant_activity_log_repo_path, grant_activity_log_repo_code)
    
    # Generate Activity Tracking Service
    activity_tracking_service_code = ActivityTrackingGenerator.generate_activity_tracking_service(package_name)
    activity_tracking_service_path = dirs['service'] / "ActivityTrackingService.java"
    write_file(activity_tracking_service_path, activity_tracking_service_code)
    
    # Generate Activity Tracking Controller
    activity_tracking_controller_code = ActivityTrackingGenerator.generate_activity_tracking_controller(package_name)
    activity_tracking_controller_path = dirs['controller'] / "ActivityTrackingController.java"
    write_file(activity_tracking_controller_path, activity_tracking_controller_code)
    
    print(f"\n>> Generating security components...")
    
    # 8. Generate Security Config
    security_config = SecurityTransformer.transform(package_name)

    web_security_props_code = SecurityGenerator.generate_web_security_properties(security_config)
    web_security_props_path = dirs['config'] / "WebSecurityProperties.java"
    write_file(web_security_props_path, web_security_props_code)

    security_code = SecurityGenerator.generate_security_config(security_config)
    security_path = dirs['config'] / "SecurityConfig.java"
    write_file(security_path, security_code)
    
    password_config_code = SecurityGenerator.generate_password_encoder_config(security_config)
    password_path = dirs['config'] / "PasswordEncoderConfig.java"
    write_file(password_path, password_config_code)
    
    # 9. Generate JWT and Authentication Components
    print(f"\n>> Generating authentication components...")
    
    jwt_config = JWTTransformer.transform(package_name)
    jwt_config_code = JWTGenerator.generate_jwt_config(jwt_config)
    jwt_config_path = dirs['auth'] / "JwtConfig.java"
    write_file(jwt_config_path, jwt_config_code)
    
    jwt_service_code = JWTGenerator.generate_jwt_service(jwt_config)
    jwt_service_path = dirs['auth'] / "JwtService.java"
    write_file(jwt_service_path, jwt_service_code)
    
    # Generate AuthService with complete login logic
    auth_service_code = AuthServiceGenerator.generate_auth_service(package_name)
    auth_service_path = dirs['service'] / "AuthService.java"
    write_file(auth_service_path, auth_service_code)
    
    # Generate updated AuthController
    auth_controller_code = AuthServiceGenerator.generate_auth_controller(package_name)
    auth_controller_path = dirs['controller'] / "AuthController.java"
    write_file(auth_controller_path, auth_controller_code)
    
    # Generate JWT Authentication Filter
    jwt_filter_code = AuthServiceGenerator.generate_jwt_filter(package_name)
    jwt_filter_path = dirs['security'] / "JwtAuthenticationFilter.java"
    write_file(jwt_filter_path, jwt_filter_code)
    
    # Generate SecurityContextHolder utility
    security_context_code = AuthServiceGenerator.generate_security_context_holder(package_name)
    security_context_path = dirs['security'] / "SecurityContextHolder.java"
    write_file(security_context_path, security_context_code)
    
    # Generate AuthorizationDeniedHandler
    auth_denied_handler_code = AuthServiceGenerator.generate_authorization_denied_handler(package_name)
    auth_denied_handler_path = dirs['security'] / "AuthorizationDeniedHandler.java"
    write_file(auth_denied_handler_path, auth_denied_handler_code)
    
    # 9.4.1. Generate Permissions Endpoint (GET /api/auth/permissions)
    print(f"\n>> Generating permissions endpoint...")
    
    # Build table→basePath entries from controller definitions
    controller_entries = []
    if layer_definitions:
        ctrl_defs = layer_definitions.get('controller_layer', {}).get('controllers', [])
        ent_defs = layer_definitions.get('entity_layer', {}).get('entities', [])
        for ctrl in ctrl_defs:
            entity_name = ctrl['entityName']
            base_path = ctrl.get('basePath', '')
            matching_entity = next((e for e in ent_defs if e['className'] == entity_name), None)
            if matching_entity and base_path:
                controller_entries.append({
                    'tableName': matching_entity['tableName'],
                    'basePath': base_path,
                })
    else:
        # Legacy mode: derive from all_entities
        for entity in all_entities:
            table_name = entity.table_name if hasattr(entity, 'table_name') else ''
            class_name = entity.class_name if hasattr(entity, 'class_name') else ''
            if table_name and class_name:
                # Convert class name to basePath: UserSkill -> /api/userSkills
                camel = class_name[0].lower() + class_name[1:]
                controller_entries.append({
                    'tableName': table_name,
                    'basePath': f'/api/{camel}s',
                })
    
    registry_code = PermissionsGenerator.generate_entity_api_registry(package_name, controller_entries)
    registry_path = dirs['service'] / "EntityApiRegistry.java"
    write_file(registry_path, registry_code)
    
    perms_service_code = PermissionsGenerator.generate_permissions_service(package_name)
    perms_service_path = dirs['service'] / "PermissionsService.java"
    write_file(perms_service_path, perms_service_code)
    
    perms_controller_code = PermissionsGenerator.generate_permissions_controller(package_name)
    perms_controller_path = dirs['controller'] / "PermissionsController.java"
    write_file(perms_controller_path, perms_controller_code)
    
    # 9.5. Generate Setup Components
    print(f"\n>> Generating setup components...")
    
    setup_controller_code = SetupGenerator.generate_setup_controller(package_name)
    setup_controller_path = dirs['controller'] / "SetupController.java"
    write_file(setup_controller_path, setup_controller_code)
    
    setup_service_code = SetupGenerator.generate_setup_service(package_name)
    setup_service_path = dirs['service'] / "SetupService.java"
    write_file(setup_service_path, setup_service_code)
    
    # Generate Thymeleaf templates
    setup_page_html = SetupGenerator.generate_setup_page()
    setup_page_path = dirs['templates'] / "setup.html"
    write_file(setup_page_path, setup_page_html)
    
    login_page_html = SetupGenerator.generate_login_page()
    login_page_path = dirs['templates'] / "login.html"
    write_file(login_page_path, login_page_html)
    
    print(f"\n>> Generating configuration files...")

    
    # 10. Generate Application Config
    app_config = ConfigTransformer.transform(db_def.projectMetadata)
    
    app_yml_code = ConfigGenerator.generate_application_yml(app_config)
    app_yml_path = dirs['src_main_resources'] / "application.yml"
    write_file(app_yml_path, app_yml_code)
    
    db_config_code = ConfigGenerator.generate_database_config(app_config)
    db_config_path = dirs['config'] / "DatabaseConfig.java"
    write_file(db_config_path, db_config_code)
    
    swagger_config_code = ConfigGenerator.generate_swagger_config(app_config)
    swagger_config_path = dirs['config'] / "SwaggerConfig.java"
    write_file(swagger_config_path, swagger_config_code)
    
    main_app_code = ConfigGenerator.generate_main_application(app_config)
    main_app_path = dirs['src_main_java'] / "Application.java"
    write_file(main_app_path, main_app_code)
    
    # 11. Generate POM
    pom_config = POMTransformer.transform(db_def.projectMetadata)
    pom_code = POMGenerator.generate(pom_config)
    pom_path = dirs['base'] / "pom.xml"
    write_file(pom_path, pom_code)
    
    # 12. Generate README
    readme_code = generate_readme(db_def.projectMetadata)
    readme_path = dirs['base'] / "README.md"
    write_file(readme_path, readme_code)
    
    # 12.5. Generate Favicon
    print(f"\n>> Generating favicon...")
    favicon_data = generate_favicon()
    favicon_path = dirs['static'] / "favicon.ico"
    write_binary_file(favicon_path, favicon_data)
    
    # 13. Generate Test Data JSON
    print(f"\n>> Generating test data...")
    test_data_json = TestDataGenerator.generate(db_def)
    test_data_path = dirs['base'] / "test-data.json"
    write_file(test_data_path, test_data_json)
    
    # 14. Generate Auth/Authz Schema SQL (with prepopulated groups from group_definition_layer)
    print(f"\n>> Generating authentication/authorization schema...")
    group_definition = None
    group_def_file = Path(output_dir) / 'application_definitions' / 'webflux_group_definition_layer.json'
    if group_def_file.exists():
        try:
            with open(group_def_file, 'r', encoding='utf-8') as f:
                group_definition = json.load(f)
            print(f"   - Loaded webflux_group_definition_layer.json ({len(group_definition.get('tableAccessGroups', []))} table groups, "
                  f"{len(group_definition.get('queryAccessGroups', []))} query groups)")
        except (json.JSONDecodeError, IOError) as e:
            print(f"   - Warning: Failed to load webflux_group_definition_layer.json: {e}")
            print(f"   - Falling back to default Super Administrators group")
    auth_schema_sql = AuthSchemaGenerator.generate(group_definition)
    auth_schema_path = dirs['base'] / "auth-schema.sql"
    write_file(auth_schema_path, auth_schema_sql)
    
    # 15. Generate Activity Tracking Schema SQL
    print(f"\n>> Generating activity tracking schema...")
    activity_tracking_schema_sql = ActivityTrackingSchemaGenerator.generate()
    activity_tracking_schema_path = dirs['base'] / "activity-tracking-schema.sql"
    write_file(activity_tracking_schema_path, activity_tracking_schema_sql)
    
    print(f"\n>> Spring WebFlux application generated successfully!")
    print(f"\n>> Next steps:")
    print(f"   1. Run the auth schema SQL:")
    print(f"      mysql -u root -p {db_def.projectMetadata.database.name} < {code_dir}/auth-schema.sql")
    print(f"   2. Run the activity tracking schema SQL:")
    print(f"      mysql -u root -p {db_def.projectMetadata.database.name} < {code_dir}/activity-tracking-schema.sql")
    print(f"   3. Build and run the application:")
    print(f"      cd {code_dir}")
    print(f"      mvn clean install")
    print(f"      mvn spring-boot:run")
    print(f"   4. Complete setup at: http://localhost:{db_def.projectMetadata.port}/setup")
    print(f"\n>> Swagger UI: http://localhost:{db_def.projectMetadata.port}/swagger-ui.html")
    print(f">> Test Data: {code_dir}/test-data.json")
    print(f">> Auth Schema: {code_dir}/auth-schema.sql")
    print(f">> Activity Tracking Schema: {code_dir}/activity-tracking-schema.sql\n")


def generate_favicon() -> bytes:
    """Generate a simple 16x16 favicon.ico file.
    
    Returns a minimal valid ICO file with a simple icon.
    """
    # This is a minimal 16x16 favicon.ico file (blue square with white border)
    # ICO format: Header + Directory Entry + BMP data
    favicon_bytes = bytes([
        # ICO Header (6 bytes)
        0x00, 0x00,  # Reserved (must be 0)
        0x01, 0x00,  # Type (1 = ICO)
        0x01, 0x00,  # Number of images
        
        # Directory Entry (16 bytes)
        0x10,        # Width (16 pixels)
        0x10,        # Height (16 pixels)
        0x00,        # Color palette (0 = no palette)
        0x00,        # Reserved
        0x01, 0x00,  # Color planes
        0x20, 0x00,  # Bits per pixel (32-bit)
        0x68, 0x04, 0x00, 0x00,  # Size of image data (1128 bytes)
        0x16, 0x00, 0x00, 0x00,  # Offset to image data (22 bytes)
        
        # BMP Header (40 bytes)
        0x28, 0x00, 0x00, 0x00,  # Header size
        0x10, 0x00, 0x00, 0x00,  # Width
        0x20, 0x00, 0x00, 0x00,  # Height (doubled for ICO)
        0x01, 0x00,              # Planes
        0x20, 0x00,              # Bits per pixel
        0x00, 0x00, 0x00, 0x00,  # Compression
        0x00, 0x04, 0x00, 0x00,  # Image size
        0x00, 0x00, 0x00, 0x00,  # X pixels per meter
        0x00, 0x00, 0x00, 0x00,  # Y pixels per meter
        0x00, 0x00, 0x00, 0x00,  # Colors used
        0x00, 0x00, 0x00, 0x00,  # Important colors
    ])
    
    # Generate 16x16 pixel data (BGRA format, bottom-up)
    # Simple blue square with white border
    pixels = []
    for y in range(16):
        for x in range(16):
            if x == 0 or x == 15 or y == 0 or y == 15:
                # White border
                pixels.extend([0xFF, 0xFF, 0xFF, 0xFF])  # BGRA
            else:
                # Blue interior
                pixels.extend([0xFF, 0x66, 0x33, 0xFF])  # BGRA (orange-blue)
    
    # Add AND mask (all transparent)
    and_mask = [0x00] * 32  # 16x16 bits = 32 bytes
    
    return favicon_bytes + bytes(pixels) + bytes(and_mask)


def generate_readme(metadata) -> str:
    """Generate README.md for the generated application."""
    return f"""# {metadata.name}

Generated Spring WebFlux Application

## Build

```bash
mvn clean install
```

## Run

```bash
mvn spring-boot:run
```

## API Documentation

Swagger UI: http://localhost:{metadata.port}/swagger-ui.html

## Database

- Type: {metadata.database.type}
- Host: {metadata.database.host}
- Port: {metadata.database.port}
- Database: {metadata.database.name}

## Authentication

This application uses JWT authentication. Register a user and login to get a JWT token.

### Register

```bash
POST /api/auth/register
{{
  "username": "user@example.com",
  "password": "password123",
  "role": "USER"
}}
```

### Login

```bash
POST /api/auth/login
{{
  "username": "user@example.com",
  "password": "password123"
}}
```

Use the returned JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Authorization

This application implements entity-level authorization with access levels:
- READ (1)
- CREATE (2)
- UPDATE (3)
- DELETE (4)
- ADMIN (5)

Higher levels include all lower level permissions.
"""


def main():
    """Main entry point (legacy single-phase mode).
    
    For two-phase workflow, use:
    - phase1_generate_definition.py (SQL/JSON -> application_definition.json)
    - phase2_generate_code.py (application_definition.json -> code)
    """
    parser = argparse.ArgumentParser(
        description='Generate Spring WebFlux application from database definition (legacy mode)'
    )
    parser.add_argument(
        '--input',
        '-i',
        required=True,
        help='Input JSON file with database definition'
    )
    parser.add_argument(
        '--output',
        '-o',
        default=None,
        help='Output directory for generated application (default: ../generated_application/<db_name>_<timestamp>)'
    )
    
    args = parser.parse_args()
    
    print("\n>> Running in LEGACY SINGLE-PHASE mode")
    print(">> For two-phase workflow, use phase1_generate_definition.py and phase2_generate_code.py\n")
    
    # Load database definition
    db_def = load_database_definition(args.input)
    
    # Generate default output path if not provided
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        db_name = db_def.projectMetadata.database.name
        args.output = f'../generated_application/{db_name}_{timestamp}'
    
    # Generate application
    generate_application(db_def, args.output)


if __name__ == '__main__':
    main()
