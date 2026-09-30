"""File storage generator - generates file storage Java code from document_storage_layer definition."""

from pathlib import Path

from templates.file_storage_templates import FileStorageTemplates
from utils.file_writer import write_file


class FileStorageGenerator:
    """Generates file storage Java code from document_storage_layer definition.

    Produces: StorageProvider, LocalStorageProvider, S3StorageProvider,
    FileMetadata, FileMetadataRepository, FileStorageService, FileController.
    Also generates entity attachment convenience methods (listFiles service method,
    GET /{id}/files controller endpoint) for each entityAttachments entry.
    """

    @staticmethod
    def generate(document_storage_layer: dict, entity_layer: dict,
                 package_name: str, dirs: dict) -> list[Path]:
        """Generate all file storage Java files.

        Args:
            document_storage_layer: Parsed webflux_document_storage_layer.json.
            entity_layer: Parsed webflux_entity_layer.json (for entity attachment validation).
            package_name: Base Java package (e.g. "com.example").
            dirs: Directory mapping from create_directory_structure().

        Returns:
            List of generated file paths.

        Raises:
            ValueError: If entityAttachments references a non-existent entity.
        """
        file_storage = document_storage_layer.get("fileStorage", {})
        if not file_storage.get("enabled", False):
            return []

        # Validate entityAttachments references against entity_layer
        entity_names = {e["className"] for e in entity_layer.get("entities", [])}
        for attachment in document_storage_layer.get("entityAttachments", []):
            entity_name = attachment["entityName"]
            if entity_name not in entity_names:
                raise ValueError(
                    f"entityAttachments references non-existent entity: '{entity_name}'"
                )

        # Create storage package directory
        storage_dir = dirs["src_main_java"] / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)

        generated = []

        # 1. StorageProvider interface
        code = FileStorageTemplates.generate_storage_provider_interface(package_name)
        path = storage_dir / "StorageProvider.java"
        write_file(path, code)
        generated.append(path)

        # 2. LocalStorageProvider
        local_base_path = file_storage.get("localBasePath", "./uploads")
        code = FileStorageTemplates.generate_local_storage_provider(package_name, local_base_path)
        path = storage_dir / "LocalStorageProvider.java"
        write_file(path, code)
        generated.append(path)

        # 3. S3StorageProvider stub
        code = FileStorageTemplates.generate_s3_storage_provider(package_name)
        path = storage_dir / "S3StorageProvider.java"
        write_file(path, code)
        generated.append(path)

        # 4. FileMetadata entity
        code = FileStorageTemplates.generate_file_metadata_entity(package_name)
        path = storage_dir / "FileMetadata.java"
        write_file(path, code)
        generated.append(path)

        # 5. FileMetadataRepository
        code = FileStorageTemplates.generate_file_metadata_repository(package_name)
        path = storage_dir / "FileMetadataRepository.java"
        write_file(path, code)
        generated.append(path)

        # 6. FileStorageService (with validation config)
        max_file_size_mb = file_storage.get("maxFileSizeMb", 50)
        allowed_content_types = file_storage.get("allowedContentTypes", [])
        code = FileStorageTemplates.generate_file_storage_service(
            package_name, max_file_size_mb, allowed_content_types
        )
        path = storage_dir / "FileStorageService.java"
        write_file(path, code)
        generated.append(path)

        # 7. FileController
        code = FileStorageTemplates.generate_file_controller(package_name)
        path = storage_dir / "FileController.java"
        write_file(path, code)
        generated.append(path)

        # Generate entity attachment convenience methods
        attachments = document_storage_layer.get("entityAttachments", [])
        for attachment in attachments:
            entity_name = attachment["entityName"]
            attachment_paths = FileStorageGenerator._generate_entity_attachment(
                entity_name, package_name, dirs
            )
            generated.extend(attachment_paths)

        return generated

    @staticmethod
    def _generate_entity_attachment(entity_name: str, package_name: str,
                                    dirs: dict) -> list[Path]:
        """Generate convenience listFiles method and GET /{id}/files endpoint for an entity.

        Generates a mixin-style service helper and controller helper in the storage package
        that delegate to FileStorageService.

        Args:
            entity_name: The entity class name (e.g. "Product").
            package_name: Base Java package.
            dirs: Directory mapping.

        Returns:
            List of generated file paths.
        """
        storage_dir = dirs["src_main_java"] / "storage"
        storage_dir.mkdir(parents=True, exist_ok=True)
        generated = []

        # Entity attachment service helper
        service_code = FileStorageGenerator._render_attachment_service(
            entity_name, package_name
        )
        service_path = storage_dir / f"{entity_name}FileService.java"
        write_file(service_path, service_code)
        generated.append(service_path)

        # Entity attachment controller helper
        controller_code = FileStorageGenerator._render_attachment_controller(
            entity_name, package_name
        )
        controller_path = storage_dir / f"{entity_name}FileController.java"
        write_file(controller_path, controller_code)
        generated.append(controller_path)

        return generated

    @staticmethod
    def _render_attachment_service(entity_name: str, package_name: str) -> str:
        """Render the entity attachment service helper with listFiles method."""
        # Convert entity name to camelCase for variable names
        entity_var = entity_name[0].lower() + entity_name[1:]
        return f"""package {package_name}.storage;

import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

/**
 * Convenience service for listing files attached to {entity_name} entities.
 * Delegates to FileStorageService.listByEntity().
 */
@Service
public class {entity_name}FileService {{

    private final FileStorageService fileStorageService;

    public {entity_name}FileService(FileStorageService fileStorageService) {{
        this.fileStorageService = fileStorageService;
    }}

    /**
     * List all files attached to a specific {entity_name} record.
     * @param entityId the ID of the {entity_name} record
     * @return Flux of FileMetadata for attached files
     */
    public Flux<FileMetadata> listFiles(Long entityId) {{
        return fileStorageService.listByEntity("{entity_name}", entityId);
    }}
}}
"""

    @staticmethod
    def _render_attachment_controller(entity_name: str, package_name: str) -> str:
        """Render the entity attachment controller with GET /{id}/files endpoint."""
        # Build basePath from entity name: "Product" -> "/api/products"
        entity_var = entity_name[0].lower() + entity_name[1:]
        base_path = f"/api/{entity_var}s"
        return f"""package {package_name}.storage;

import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

/**
 * REST controller providing file listing endpoint for {entity_name} entities.
 * Exposes GET {base_path}/{{id}}/files to list attached files.
 */
@RestController
@RequestMapping("{base_path}")
public class {entity_name}FileController {{

    private final {entity_name}FileService {entity_var}FileService;

    public {entity_name}FileController({entity_name}FileService {entity_var}FileService) {{
        this.{entity_var}FileService = {entity_var}FileService;
    }}

    /**
     * List all files attached to a {entity_name} record.
     * GET {base_path}/{{id}}/files
     */
    @GetMapping("/{{id}}/files")
    public Flux<FileMetadata> listFiles(@PathVariable Long id) {{
        return {entity_var}FileService.listFiles(id);
    }}
}}
"""
