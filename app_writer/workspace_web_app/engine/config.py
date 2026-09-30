"""Engine Service configuration — workspace paths, Kafka config, tool locations."""

import os

# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

CONSUME_TOPICS = ["commands.tools", "commands.agent", "commands.jobs"]
PRODUCE_TOPICS = ["results.tools", "results.agent", "events.jobs", "events.status"]

KAFKA_GROUP_ID = "engine-service"

# Workspace
WORKSPACE_ROOT = os.getenv("WORKSPACE_ROOT", "/workspace")

# Tool locations (relative to WORKSPACE_ROOT)
TOOL_PATHS = {
    "app_def_manager": "app_def_manager/cli.py",
    "swfaw": "swfaw/generate_app.py",
    "phase3": "swfaw/phase3_definition_first.py",
    "reaw": "reaw/generate_react_app.py",
    "definition_editor": "definition_editor/cli.py",
    "db_manager": "db_manager/db_manager.py",
    "app_validator": "app_validator/validate.py",
    "theme_scraper": "theme_scraper/scrape.py",
    "dummy_data": "dummy_data_generator/main.py",
    "discussion_tracker": "discussion_tracker/cli.py",
    "github_crawler": "github_crawler",
}

# Application definitions
APPLICATION_DEFINITIONS_DIR = os.path.join(WORKSPACE_ROOT, "application_definitions")

# Engine Service
ENGINE_HOST = "0.0.0.0"
ENGINE_PORT = 8000

# AI config
AI_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "ai_config.yaml")
