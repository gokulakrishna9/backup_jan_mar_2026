"""File writing utilities for generated code."""

import os
from pathlib import Path
from typing import Optional


def create_directory_structure(base_path: str, package_name: str) -> dict:
    """Create the directory structure for a Spring WebFlux application.
    
    Args:
        base_path: Base output directory
        package_name: Java package name (e.g., 'com.example')
        
    Returns:
        Dictionary with paths to each directory
    """
    base = Path(base_path)
    
    # Convert package name to path
    package_path = package_name.replace('.', '/')
    
    # Define directory structure
    dirs = {
        'base': base,
        'src_main_java': base / 'src' / 'main' / 'java' / package_path,
        'src_main_resources': base / 'src' / 'main' / 'resources',
        'src_test_java': base / 'src' / 'test' / 'java' / package_path,
        'entity': base / 'src' / 'main' / 'java' / package_path / 'entity',
        'dto': base / 'src' / 'main' / 'java' / package_path / 'dto',
        'model': base / 'src' / 'main' / 'java' / package_path / 'model',
        'repository': base / 'src' / 'main' / 'java' / package_path / 'repository',
        'service': base / 'src' / 'main' / 'java' / package_path / 'service',
        'controller': base / 'src' / 'main' / 'java' / package_path / 'controller',
        'security': base / 'src' / 'main' / 'java' / package_path / 'security',
        'auth': base / 'src' / 'main' / 'java' / package_path / 'auth',
        'config': base / 'src' / 'main' / 'java' / package_path / 'config',
        'exception': base / 'src' / 'main' / 'java' / package_path / 'exception',
        'templates': base / 'src' / 'main' / 'resources' / 'templates',
        'templates_admin': base / 'src' / 'main' / 'resources' / 'templates' / 'admin',
        'static': base / 'src' / 'main' / 'resources' / 'static',
        'test_service': base / 'src' / 'test' / 'java' / package_path / 'service',
        'test_controller': base / 'src' / 'test' / 'java' / package_path / 'controller',
    }
    
    # Create all directories
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return dirs


def write_file(file_path: str, content: str, base_path: Optional[str] = None) -> None:
    """Write content to a file.
    
    Args:
        file_path: Relative or absolute file path
        content: File content to write
        base_path: Optional base path to prepend
    """
    if base_path:
        full_path = Path(base_path) / file_path
    else:
        full_path = Path(file_path)
    
    # Create parent directories if they don't exist
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write content
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] Generated: {full_path}")


def write_binary_file(file_path: str, content: bytes, base_path: Optional[str] = None) -> None:
    """Write binary content to a file.
    
    Args:
        file_path: Relative or absolute file path
        content: Binary content to write
        base_path: Optional base path to prepend
    """
    if base_path:
        full_path = Path(base_path) / file_path
    else:
        full_path = Path(file_path)
    
    # Create parent directories if they don't exist
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write binary content
    with open(full_path, 'wb') as f:
        f.write(content)
    
    print(f"[OK] Generated: {full_path}")


def get_java_file_path(package_name: str, layer: str, class_name: str) -> str:
    """Get the relative path for a Java file.
    
    Args:
        package_name: Java package (e.g., 'com.example')
        layer: Layer name (entity, dto, service, etc.)
        class_name: Java class name
        
    Returns:
        Relative file path
    """
    package_path = package_name.replace('.', '/')
    return f"src/main/java/{package_path}/{layer}/{class_name}.java"


def get_test_file_path(package_name: str, layer: str, class_name: str) -> str:
    """Get the relative path for a test file.
    
    Args:
        package_name: Java package (e.g., 'com.example')
        layer: Layer name (service, controller, etc.)
        class_name: Test class name
        
    Returns:
        Relative file path
    """
    package_path = package_name.replace('.', '/')
    return f"src/test/java/{package_path}/{layer}/{class_name}.java"
