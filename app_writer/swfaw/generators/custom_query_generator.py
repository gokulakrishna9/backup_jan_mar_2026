"""Custom query generator - populates custom query templates."""

from jinja2 import Template
from typing import List, Dict, Any
from models.layer_objects import QueryLayerObject, FilterLayerObject
from templates.custom_query_templates import CustomQueryTemplates


class CustomQueryGenerator:
    """Generates custom query Java code from query and filter layer objects."""
    
    @staticmethod
    def generate_query_result_dto(query_name: str, query_def: Dict[str, Any], package_name: str) -> str:
        """Generate query result DTO.
        
        Args:
            query_name: Name of the query
            query_def: Query definition dictionary
            package_name: Base package name
            
        Returns:
            Generated Java code as string
        """
        # Parse select fields to determine DTO fields
        fields = []
        imports = set()
        
        for select_field in query_def.get('select', []):
            # Parse field (e.g., "u.id", "u.username", "COUNT(r.id) as role_count")
            parts = select_field.split(' as ')
            if len(parts) == 2:
                field_name = parts[1].strip()
            else:
                # Extract field name from "table.field"
                field_parts = select_field.split('.')
                if len(field_parts) == 2:
                    field_name = field_parts[1].strip()
                else:
                    field_name = select_field.strip()
            
            # Determine field type (simplified - would need more logic in production)
            field_type = "String"  # Default
            if 'COUNT' in select_field or 'SUM' in select_field:
                field_type = "Long"
            elif 'AVG' in select_field:
                field_type = "Double"
            elif '_id' in field_name.lower():
                field_type = "Long"
            elif '_date' in field_name.lower() or 'created' in field_name.lower() or 'updated' in field_name.lower():
                field_type = "LocalDateTime"
                imports.add("java.time.LocalDateTime")
            elif '_active' in field_name.lower() or 'is_' in field_name.lower():
                field_type = "Boolean"
            
            fields.append({
                'name': CustomQueryGenerator._to_camel_case(field_name),
                'type': field_type
            })
        
        context = {
            'packageName': f"{package_name}.dto",
            'className': query_def.get('returnType', f"{CustomQueryGenerator._to_pascal_case(query_name)}DTO"),
            'queryName': query_name,
            'description': query_def.get('description', ''),
            'fields': fields,
            'imports': sorted(list(imports))
        }
        
        template = Template(CustomQueryTemplates.QUERY_RESULT_DTO_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_custom_query_repository(query_layer: QueryLayerObject, package_name: str) -> str:
        """Generate custom query repository.
        
        Args:
            query_layer: Query layer object
            package_name: Base package name
            
        Returns:
            Generated Java code as string
        """
        imports = set()
        imports.add("java.time.LocalDateTime")
        imports.add("java.time.LocalDate")
        imports.add("java.time.LocalTime")
        imports.add("java.math.BigDecimal")
        imports.add("java.util.List")
        
        # Process queries
        processed_queries = []
        for query in query_layer.queries:
            # Build SQL from query definition
            sql = CustomQueryGenerator._build_sql(query)
            count_sql = CustomQueryGenerator._build_count_sql(query)
            
            # Parse result fields from select
            result_fields = []
            for select_field in query.select:
                parts = select_field.split(' as ')
                if len(parts) == 2:
                    column_name = parts[1].strip()
                    field_name = CustomQueryGenerator._to_camel_case(column_name)
                else:
                    field_parts = select_field.split('.')
                    if len(field_parts) == 2:
                        column_name = field_parts[1].strip()
                        field_name = CustomQueryGenerator._to_camel_case(column_name)
                    else:
                        column_name = select_field.strip()
                        field_name = CustomQueryGenerator._to_camel_case(column_name)
                
                # Determine type
                field_type = "String"
                if '_id' in column_name.lower():
                    field_type = "Long"
                elif '_date' in column_name.lower() or 'created' in column_name.lower() or 'updated' in column_name.lower():
                    field_type = "LocalDateTime"
                elif '_active' in column_name.lower() or 'is_' in column_name.lower():
                    field_type = "Boolean"
                
                result_fields.append({
                    'name': field_name,
                    'columnName': column_name,
                    'type': field_type
                })
            
            processed_queries.append({
                'name': query.name,
                'description': query.description,
                'returnType': query.returnType,
                'sql': sql,
                'countSql': count_sql,
                'parameters': [p.model_dump() for p in query.parameters],
                'pagination': query.pagination,
                'resultFields': result_fields
            })
        
        context = {
            'packageName': f"{package_name}.repository",
            'className': f"{query_layer.entityName}CustomQueryRepository",
            'entityName': query_layer.entityName,
            'queries': processed_queries,
            'imports': sorted(list(imports))
        }
        
        template = Template(CustomQueryTemplates.CUSTOM_QUERY_REPOSITORY_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_custom_query_service(query_layer: QueryLayerObject, package_name: str) -> str:
        """Generate custom query service.
        
        Args:
            query_layer: Query layer object
            package_name: Base package name
            
        Returns:
            Generated Java code as string
        """
        imports = set()
        imports.add(f"{package_name}.dto.*")
        
        has_authorization = any(q.authorization.get('enabled', False) for q in query_layer.queries)
        
        # Process queries
        processed_queries = []
        for query in query_layer.queries:
            auth_config = query.authorization if query.authorization else {}
            
            processed_query = {
                'name': query.name,
                'description': query.description,
                'returnType': query.returnType,
                'parameters': [p.model_dump() for p in query.parameters],
                'pagination': query.pagination,
                'authorization': {
                    'enabled': auth_config.get('enabled', False),
                    'documentField': auth_config.get('documentField', 'id'),
                    'documentFieldType': 'Long'  # Simplified
                }
            }
            processed_queries.append(processed_query)
        
        context = {
            'packageName': f"{package_name}.service",
            'repositoryPackage': f"{package_name}.repository",
            'securityPackage': f"{package_name}.security",
            'className': f"{query_layer.entityName}CustomQueryService",
            'repositoryName': f"{query_layer.entityName}CustomQueryRepository",
            'entityName': query_layer.entityName,
            'queries': processed_queries,
            'hasAuthorization': has_authorization,
            'imports': sorted(list(imports))
        }
        
        template = Template(CustomQueryTemplates.CUSTOM_QUERY_SERVICE_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_custom_query_controller(query_layer: QueryLayerObject, package_name: str) -> str:
        """Generate custom query controller.
        
        Args:
            query_layer: Query layer object
            package_name: Base package name
            
        Returns:
            Generated Java code as string
        """
        imports = set()
        imports.add(f"{package_name}.dto.*")
        
        # Process queries for controller endpoints
        processed_queries = []
        for query in query_layer.queries:
            auth_config = query.authorization if query.authorization else {}
            
            # Determine HTTP method and path
            http_method = "GetMapping"
            path = f"/queries/{CustomQueryGenerator._to_kebab_case(query.name)}"
            
            processed_query = {
                'name': query.name,
                'description': query.description,
                'returnType': query.returnType,
                'httpMethod': http_method,
                'path': path,
                'parameters': [
                    {
                        **p.model_dump(),
                        'pathVariable': False  # All query params for now
                    }
                    for p in query.parameters
                ],
                'pagination': query.pagination,
                'authorization': {
                    'enabled': auth_config.get('enabled', False)
                }
            }
            processed_queries.append(processed_query)
        
        entity_name_lower = query_layer.entityName[0].lower() + query_layer.entityName[1:]
        
        context = {
            'packageName': f"{package_name}.controller",
            'servicePackage': f"{package_name}.service",
            'dtoPackage': f"{package_name}.dto",
            'className': f"{query_layer.entityName}CustomQueryController",
            'serviceName': f"{query_layer.entityName}CustomQueryService",
            'filterDtoName': f"{query_layer.entityName}FilterDTO",
            'entityName': query_layer.entityName,
            'basePath': f"/api/{entity_name_lower}",
            'queries': processed_queries,
            'imports': sorted(list(imports))
        }
        
        template = Template(CustomQueryTemplates.CUSTOM_QUERY_CONTROLLER_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_filter_dto(filter_layer: FilterLayerObject, package_name: str) -> str:
        """Generate filter DTO.
        
        Args:
            filter_layer: Filter layer object
            package_name: Base package name
            
        Returns:
            Generated Java code as string
        """
        imports = set()
        imports.add("java.util.List")
        
        # Add imports based on field types
        for field in filter_layer.fields:
            if field.type == "LocalDateTime":
                imports.add("java.time.LocalDateTime")
            elif field.type == "LocalDate":
                imports.add("java.time.LocalDate")
            elif field.type == "LocalTime":
                imports.add("java.time.LocalTime")
            elif field.type == "BigDecimal":
                imports.add("java.math.BigDecimal")
        
        context = {
            'packageName': f"{package_name}.dto",
            'className': f"{filter_layer.entityName}FilterDTO",
            'entityName': filter_layer.entityName,
            'fields': [f.model_dump() for f in filter_layer.fields],
            'imports': sorted(list(imports))
        }
        
        template = Template(CustomQueryTemplates.FILTER_DTO_TEMPLATE)
        return template.render(context)
    
    # Helper methods
    
    @staticmethod
    def _build_sql(query) -> str:
        """Build SQL query from query definition."""
        sql_parts = []
        
        # SELECT
        sql_parts.append(f"SELECT {', '.join(query.select)}")
        
        # FROM
        sql_parts.append(f"FROM {query.from_}")
        
        # JOINS
        for join in query.joins:
            alias = f" {join.alias}" if join.alias else ""
            sql_parts.append(f"{join.type} JOIN {join.table}{alias} ON {join.on}")
        
        # WHERE
        if query.where:
            sql_parts.append(f"WHERE {' AND '.join(query.where)}")
        
        # GROUP BY
        if query.groupBy:
            sql_parts.append(f"GROUP BY {', '.join(query.groupBy)}")
        
        # HAVING
        if query.having:
            sql_parts.append(f"HAVING {' AND '.join(query.having)}")
        
        # ORDER BY
        if query.orderBy:
            sql_parts.append(f"ORDER BY {', '.join(query.orderBy)}")
        
        return " ".join(sql_parts)
    
    @staticmethod
    def _build_count_sql(query) -> str:
        """Build COUNT SQL query from query definition."""
        sql_parts = []
        
        # SELECT COUNT
        sql_parts.append("SELECT COUNT(*)")
        
        # FROM
        sql_parts.append(f"FROM {query.from_}")
        
        # JOINS
        for join in query.joins:
            alias = f" {join.alias}" if join.alias else ""
            sql_parts.append(f"{join.type} JOIN {join.table}{alias} ON {join.on}")
        
        # WHERE
        if query.where:
            sql_parts.append(f"WHERE {' AND '.join(query.where)}")
        
        return " ".join(sql_parts)
    
    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def _to_pascal_case(snake_str: str) -> str:
        """Convert snake_case to PascalCase."""
        return ''.join(x.title() for x in snake_str.split('_'))
    
    @staticmethod
    def _to_kebab_case(camel_str: str) -> str:
        """Convert camelCase to kebab-case."""
        import re
        return re.sub(r'(?<!^)(?=[A-Z])', '-', camel_str).lower()
