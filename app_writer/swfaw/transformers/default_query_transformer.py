"""Default query transformer - generates intelligent default queries based on table relationships."""

from typing import List, Dict, Any, Set, Tuple
from models.layer_objects import EntityLayerObject, QueryLayerObject, CustomQuery, QueryParameter, QueryJoin
from models.database_definition import Table, Relationship


class DefaultQueryTransformer:
    """Transforms entity relationships into intelligent default queries.
    
    Query Generation Rules:
    1. Leaf Tables (no children): Generate queries with master table label columns
    2. Master Tables (have children): Generate grouping queries with child record counts
    3. Linked Tables (ManyToMany): Generate two queries, treating each side as master
    """
    
    def __init__(self, tables: List[Table], entities: List[EntityLayerObject], package_name: str = "com.example"):
        """Initialize the transformer.
        
        Args:
            tables: List of all database tables
            entities: List of all entity layer objects
            package_name: Base package name
        """
        self.tables = {t.name: t for t in tables}
        self.entities = {e.tableName: e for e in entities}
        self.package_name = package_name
        
        # Build relationship maps
        self._build_relationship_maps()
    
    def _build_relationship_maps(self):
        """Build maps of outgoing and incoming relationships for each table."""
        self.outgoing_rels: Dict[str, List[Relationship]] = {}
        self.incoming_rels: Dict[str, List[Dict[str, Any]]] = {}
        
        for table_name, table in self.tables.items():
            self.outgoing_rels[table_name] = table.relationships
            
            # Build incoming relationships
            for rel in table.relationships:
                target = rel.targetTable
                if target not in self.incoming_rels:
                    self.incoming_rels[target] = []
                
                self.incoming_rels[target].append({
                    'sourceTable': table_name,
                    'type': rel.type,
                    'foreignKey': rel.foreignKey,
                    'referencedColumn': getattr(rel, 'referencedColumn', 'id')
                })
    
    def transform(self) -> List[QueryLayerObject]:
        """Transform all entities into query layer objects with default queries.
        
        Returns:
            List of QueryLayerObject with generated queries
        """
        query_layers = []
        
        for table_name, entity in self.entities.items():
            queries = []
            
            # Determine table type and generate appropriate queries
            is_leaf = self._is_leaf_table(table_name)
            is_master = self._is_master_table(table_name)
            is_linked = self._is_linked_table(table_name)
            
            if is_leaf:
                queries.extend(self._generate_leaf_queries(table_name, entity))
            
            if is_master:
                queries.extend(self._generate_master_queries(table_name, entity))
            
            if is_linked:
                queries.extend(self._generate_linked_queries(table_name, entity))
            
            # Always generate basic list query
            queries.insert(0, self._generate_basic_list_query(table_name, entity))
            
            query_layer = QueryLayerObject(
                entityName=entity.className,
                queries=queries,
                packageName=f"{self.package_name}.query"
            )
            query_layers.append(query_layer)
        
        return query_layers
    
    def _is_leaf_table(self, table_name: str) -> bool:
        """Check if table is a leaf (has no children)."""
        outgoing = self.outgoing_rels.get(table_name, [])
        # Leaf if has no OneToMany relationships
        return not any(rel.type == 'OneToMany' for rel in outgoing)
    
    def _is_master_table(self, table_name: str) -> bool:
        """Check if table is a master (has children)."""
        outgoing = self.outgoing_rels.get(table_name, [])
        # Master if has OneToMany relationships
        return any(rel.type == 'OneToMany' for rel in outgoing)
    
    def _is_linked_table(self, table_name: str) -> bool:
        """Check if table is a linking table (ManyToMany)."""
        outgoing = self.outgoing_rels.get(table_name, [])
        incoming = self.incoming_rels.get(table_name, [])
        
        # Linked if has ManyToMany relationships
        has_many_to_many_out = any(rel.type == 'ManyToMany' for rel in outgoing)
        has_many_to_many_in = any(rel['type'] == 'ManyToMany' for rel in incoming)
        
        return has_many_to_many_out or has_many_to_many_in
    
    def _generate_basic_list_query(self, table_name: str, entity: EntityLayerObject) -> CustomQuery:
        """Generate basic list all query."""
        table = self.tables[table_name]
        entity_alias = table_name[0].lower()
        
        # Get all columns for select
        select_fields = [f"{entity_alias}.{col.name}" for col in table.columns]
        
        return CustomQuery(
            name=f"list{entity.className}",
            description=f"List all {entity.className} records",
            returnType=f"{entity.className}OutputDTO",
            select=select_fields,
            from_=f"{table_name} {entity_alias}",
            joins=[],
            where=[],
            groupBy=[],
            having=[],
            orderBy=[f"{entity_alias}.id DESC"],
            pagination=True,
            parameters=[],
            authorization={'enabled': True, 'documentField': 'id'}
        )
    
    def _generate_leaf_queries(self, table_name: str, entity: EntityLayerObject) -> List[CustomQuery]:
        """Generate queries for leaf tables with master label columns."""
        queries = []
        table = self.tables[table_name]
        entity_alias = table_name[0].lower()
        
        # Find all master relationships (ManyToOne)
        master_rels = [rel for rel in self.outgoing_rels.get(table_name, []) 
                      if rel.type == 'ManyToOne']
        
        if not master_rels:
            return queries
        
        # Generate query with all master labels
        select_fields = [f"{entity_alias}.{col.name}" for col in table.columns]
        joins = []
        
        for i, rel in enumerate(master_rels):
            master_table = self.tables.get(rel.targetTable)
            if not master_table:
                continue
            
            master_alias = f"m{i+1}"
            label_col = self._find_label_column(master_table)
            
            # Add master label to select
            select_fields.append(f"{master_alias}.{label_col} as {rel.targetTable}_{label_col}")
            
            # Add join
            joins.append(QueryJoin(
                type="LEFT",
                table=rel.targetTable,
                alias=master_alias,
                on=f"{entity_alias}.{rel.foreignKey} = {master_alias}.id"
            ))
        
        queries.append(CustomQuery(
            name=f"list{entity.className}WithMasters",
            description=f"List {entity.className} with master table labels",
            returnType=f"{entity.className}WithMastersDTO",
            select=select_fields,
            from_=f"{table_name} {entity_alias}",
            joins=joins,
            where=[],
            groupBy=[],
            having=[],
            orderBy=[f"{entity_alias}.id DESC"],
            pagination=True,
            parameters=[],
            authorization={'enabled': True, 'documentField': 'id'}
        ))
        
        # Generate filtered queries by each master
        for i, rel in enumerate(master_rels):
            master_table = self.tables.get(rel.targetTable)
            if not master_table:
                continue
            
            master_class = self._to_pascal_case(rel.targetTable)
            
            queries.append(CustomQuery(
                name=f"list{entity.className}By{master_class}",
                description=f"List {entity.className} filtered by {master_class}",
                returnType=f"{entity.className}OutputDTO",
                select=[f"{entity_alias}.{col.name}" for col in table.columns],
                from_=f"{table_name} {entity_alias}",
                joins=[],
                where=[f"{entity_alias}.{rel.foreignKey} = :{self._to_camel_case(rel.foreignKey)}"],
                groupBy=[],
                having=[],
                orderBy=[f"{entity_alias}.id DESC"],
                pagination=True,
                parameters=[
                    QueryParameter(
                        name=self._to_camel_case(rel.foreignKey),
                        type="Long",
                        required=True
                    )
                ],
                authorization={'enabled': True, 'documentField': 'id'}
            ))
        
        return queries
    
    def _generate_master_queries(self, table_name: str, entity: EntityLayerObject) -> List[CustomQuery]:
        """Generate grouping queries for master tables with child counts."""
        queries = []
        table = self.tables[table_name]
        entity_alias = table_name[0].lower()
        
        # Find all child relationships (OneToMany)
        child_rels = [rel for rel in self.outgoing_rels.get(table_name, []) 
                     if rel.type == 'OneToMany']
        
        if not child_rels:
            return queries
        
        # Get label column for master
        label_col = self._find_label_column(table)
        
        # Generate query with counts for all children
        select_fields = [
            f"{entity_alias}.id",
            f"{entity_alias}.{label_col}"
        ]
        joins = []
        
        for i, rel in enumerate(child_rels):
            child_alias = f"c{i+1}"
            child_class = self._to_pascal_case(rel.targetTable)
            
            # Add count to select
            select_fields.append(f"COUNT(DISTINCT {child_alias}.id) as {self._to_camel_case(rel.targetTable)}_count")
            
            # Add join
            joins.append(QueryJoin(
                type="LEFT",
                table=rel.targetTable,
                alias=child_alias,
                on=f"{entity_alias}.id = {child_alias}.{rel.foreignKey}"
            ))
        
        queries.append(CustomQuery(
            name=f"list{entity.className}WithChildCounts",
            description=f"List {entity.className} with counts of all child records",
            returnType=f"{entity.className}WithCountsDTO",
            select=select_fields,
            from_=f"{table_name} {entity_alias}",
            joins=joins,
            where=[],
            groupBy=[f"{entity_alias}.id", f"{entity_alias}.{label_col}"],
            having=[],
            orderBy=[f"{entity_alias}.id DESC"],
            pagination=True,
            parameters=[],
            authorization={'enabled': True, 'documentField': 'id'}
        ))
        
        # Generate individual child count queries
        for rel in child_rels:
            child_class = self._to_pascal_case(rel.targetTable)
            child_alias = "c"
            
            queries.append(CustomQuery(
                name=f"list{entity.className}With{child_class}Count",
                description=f"List {entity.className} with {child_class} count",
                returnType=f"{entity.className}With{child_class}CountDTO",
                select=[
                    f"{entity_alias}.id",
                    f"{entity_alias}.{label_col}",
                    f"COUNT({child_alias}.id) as {self._to_camel_case(rel.targetTable)}_count"
                ],
                from_=f"{table_name} {entity_alias}",
                joins=[
                    QueryJoin(
                        type="LEFT",
                        table=rel.targetTable,
                        alias=child_alias,
                        on=f"{entity_alias}.id = {child_alias}.{rel.foreignKey}"
                    )
                ],
                where=[],
                groupBy=[f"{entity_alias}.id", f"{entity_alias}.{label_col}"],
                having=[],
                orderBy=[f"{entity_alias}.id DESC"],
                pagination=True,
                parameters=[],
                authorization={'enabled': True, 'documentField': 'id'}
            ))
        
        return queries
    
    def _generate_linked_queries(self, table_name: str, entity: EntityLayerObject) -> List[CustomQuery]:
        """Generate queries for linked tables, treating each side as master."""
        queries = []
        table = self.tables[table_name]
        entity_alias = table_name[0].lower()
        
        # Find ManyToMany relationships
        many_to_many_rels = [rel for rel in self.outgoing_rels.get(table_name, []) 
                            if rel.type == 'ManyToMany']
        
        # Also check incoming ManyToMany
        incoming = self.incoming_rels.get(table_name, [])
        incoming_many_to_many = [rel for rel in incoming if rel['type'] == 'ManyToMany']
        
        # Generate queries for outgoing ManyToMany
        for rel in many_to_many_rels:
            target_table = self.tables.get(rel.targetTable)
            if not target_table:
                continue
            
            target_class = self._to_pascal_case(rel.targetTable)
            target_label = self._find_label_column(target_table)
            
            # Query 1: List linked table with target labels
            queries.append(CustomQuery(
                name=f"list{entity.className}With{target_class}",
                description=f"List {entity.className} with linked {target_class} information",
                returnType=f"{entity.className}With{target_class}DTO",
                select=[
                    f"{entity_alias}.*",
                    f"t.{target_label} as {rel.targetTable}_{target_label}"
                ],
                from_=f"{table_name} {entity_alias}",
                joins=[
                    QueryJoin(
                        type="LEFT",
                        table=rel.targetTable,
                        alias="t",
                        on=f"{entity_alias}.{rel.foreignKey} = t.id"
                    )
                ],
                where=[],
                groupBy=[],
                having=[],
                orderBy=[f"{entity_alias}.id DESC"],
                pagination=True,
                parameters=[],
                authorization={'enabled': True, 'documentField': 'id'}
            ))
            
            # Query 2: List target with linked table labels (reverse perspective)
            source_label = self._find_label_column(table)
            
            queries.append(CustomQuery(
                name=f"list{target_class}With{entity.className}",
                description=f"List {target_class} with linked {entity.className} information",
                returnType=f"{target_class}With{entity.className}DTO",
                select=[
                    f"t.*",
                    f"{entity_alias}.{source_label} as {table_name}_{source_label}"
                ],
                from_=f"{rel.targetTable} t",
                joins=[
                    QueryJoin(
                        type="LEFT",
                        table=table_name,
                        alias=entity_alias,
                        on=f"t.id = {entity_alias}.{rel.foreignKey}"
                    )
                ],
                where=[],
                groupBy=[],
                having=[],
                orderBy=["t.id DESC"],
                pagination=True,
                parameters=[],
                authorization={'enabled': True, 'documentField': 'id'}
            ))
        
        return queries
    
    def _find_label_column(self, table: Table) -> str:
        """Find the best label column for a table.
        
        Priority: name > title > label > description > first non-id string column
        """
        label_candidates = ['name', 'title', 'label', 'description', 'username', 'email']
        
        for candidate in label_candidates:
            for col in table.columns:
                if col.name.lower() == candidate:
                    return col.name
        
        # Fallback to first non-id string column
        for col in table.columns:
            if not col.primaryKey and 'VARCHAR' in col.type.upper():
                return col.name
        
        # Last resort: use id
        return 'id'
    
    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def _to_pascal_case(snake_str: str) -> str:
        """Convert snake_case to PascalCase."""
        return ''.join(x.title() for x in snake_str.split('_'))
