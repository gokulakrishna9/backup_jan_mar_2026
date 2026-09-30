"""
Dependency Analyzer - Determines table generation order based on foreign keys
"""

from typing import Dict, List, Set
from sql_parser import Table


class DependencyAnalyzer:
    def __init__(self, tables: Dict[str, Table]):
        self.tables = tables
        self.dependencies = self._build_dependency_graph()
    
    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """Build a graph of table dependencies (table -> tables it depends on)"""
        graph = {table_name: set() for table_name in self.tables}
        
        for table_name, table in self.tables.items():
            for fk in table.foreign_keys:
                if fk.ref_table in self.tables and fk.ref_table != table_name:
                    graph[table_name].add(fk.ref_table)
        
        return graph
    
    def get_generation_order(self) -> List[str]:
        """Return tables in topological order (dependencies first)"""
        visited = set()
        order = []
        
        def visit(table_name: str):
            if table_name in visited:
                return
            visited.add(table_name)
            
            # Visit dependencies first
            for dep in self.dependencies.get(table_name, set()):
                visit(dep)
            
            order.append(table_name)
        
        for table_name in self.tables:
            visit(table_name)
        
        return order
    
    def get_dependents(self, table_name: str) -> Set[str]:
        """Get tables that depend on this table"""
        dependents = set()
        for tbl, deps in self.dependencies.items():
            if table_name in deps:
                dependents.add(tbl)
        return dependents
    
    def is_leaf_table(self, table_name: str) -> bool:
        """Check if table has no dependents (leaf in dependency tree)"""
        return len(self.get_dependents(table_name)) == 0
    
    def get_depth(self, table_name: str) -> int:
        """Get depth in dependency tree (0 = no dependencies)"""
        if not self.dependencies.get(table_name):
            return 0
        return 1 + max(self.get_depth(dep) for dep in self.dependencies[table_name])
