"""JSON column generator - generates JSON converter and document collection Java code from document_storage_layer definition."""

from pathlib import Path

from templates.json_column_templates import JsonColumnTemplates
from templates.document_collection_templates import DocumentCollectionTemplates
from utils.file_writer import write_file


class JsonColumnGenerator:
    """Generates JSON column converters and document collection code from definition.

    Produces: JsonReadingConverter, JsonWritingConverter, R2dbcJsonConversionsConfig
    (when jsonColumns is non-empty), and per-collection entity, repository, service,
    controller, input DTO, output DTO (when documentCollections is non-empty).
    """

    @staticmethod
    def generate(document_storage_layer: dict, entity_layer: dict,
                 package_name: str, dirs: dict) -> list[Path]:
        """Generate JSON converter + document collection Java files.

        Args:
            document_storage_layer: Parsed webflux_document_storage_layer.json.
            entity_layer: Parsed webflux_entity_layer.json (for entity validation).
            package_name: Base Java package.
            dirs: Directory mapping from create_directory_structure().

        Returns:
            List of generated file paths.

        Raises:
            ValueError: If jsonColumns references a non-existent entity.
        """
        json_columns = document_storage_layer.get("jsonColumns", [])
        collections = document_storage_layer.get("documentCollections", [])

        if not json_columns and not collections:
            return []

        # Validate jsonColumns entity references against entity_layer
        entity_names = {e["className"] for e in entity_layer.get("entities", [])}
        for jc in json_columns:
            entity_name = jc["entityName"]
            if entity_name not in entity_names:
                raise ValueError(
                    f"jsonColumns references non-existent entity: '{entity_name}'"
                )

        generated = []

        # Generate converter files when jsonColumns is non-empty
        if json_columns:
            converter_dir = dirs["src_main_java"] / "converter"
            converter_dir.mkdir(parents=True, exist_ok=True)

            # 1. JsonReadingConverter
            code = JsonColumnTemplates.generate_json_reading_converter(package_name)
            path = converter_dir / "JsonReadingConverter.java"
            write_file(path, code)
            generated.append(path)

            # 2. JsonWritingConverter
            code = JsonColumnTemplates.generate_json_writing_converter(package_name)
            path = converter_dir / "JsonWritingConverter.java"
            write_file(path, code)
            generated.append(path)

            # 3. R2dbcJsonConversionsConfig
            code = JsonColumnTemplates.generate_r2dbc_json_conversions_config(package_name)
            path = converter_dir / "R2dbcJsonConversionsConfig.java"
            write_file(path, code)
            generated.append(path)

        # Generate document collection files (6 per collection)
        if collections:
            document_dir = dirs["src_main_java"] / "document"
            document_dir.mkdir(parents=True, exist_ok=True)

            for collection in collections:
                collection_name = collection["name"]
                table_name = collection["tableName"]

                # 1. Entity
                code = DocumentCollectionTemplates.generate_collection_entity(
                    package_name, collection_name, table_name
                )
                path = document_dir / f"{collection_name}.java"
                write_file(path, code)
                generated.append(path)

                # 2. Repository
                code = DocumentCollectionTemplates.generate_collection_repository(
                    package_name, collection_name, table_name
                )
                path = document_dir / f"{collection_name}Repository.java"
                write_file(path, code)
                generated.append(path)

                # 3. Service
                code = DocumentCollectionTemplates.generate_collection_service(
                    package_name, collection_name, table_name
                )
                path = document_dir / f"{collection_name}Service.java"
                write_file(path, code)
                generated.append(path)

                # 4. Controller
                code = DocumentCollectionTemplates.generate_collection_controller(
                    package_name, collection_name, table_name
                )
                path = document_dir / f"{collection_name}Controller.java"
                write_file(path, code)
                generated.append(path)

                # 5. Input DTO
                code = DocumentCollectionTemplates.generate_collection_input_dto(
                    package_name, collection_name, table_name
                )
                path = document_dir / f"{collection_name}InputDTO.java"
                write_file(path, code)
                generated.append(path)

                # 6. Output DTO
                code = DocumentCollectionTemplates.generate_collection_output_dto(
                    package_name, collection_name, table_name
                )
                path = document_dir / f"{collection_name}OutputDTO.java"
                write_file(path, code)
                generated.append(path)

        return generated
