"""App Def Manager REST endpoints — thin Kafka gateway.

Every endpoint is a one-liner delegating to publish_and_await.
No tool logic lives here; the Engine Service handles execution.
Destructive operations require ``confirm=true`` query parameter (Req 12.2).
"""

from fastapi import APIRouter, Depends, HTTPException, Query

from workspace_web_app.ui_service.main import get_correlation_store, get_producer
from workspace_web_app.ui_service.models.requests import (
    AddEndpointRequest,
    AddEntityRequest,
    AddFieldRequest,
    AddQueryRequest,
    AddRelationshipRequest,
    BulkUpdateRequest,
    ModifyFieldRequest,
    ScaffoldAppRequest,
)
from workspace_web_app.ui_service.utils.kafka_rpc import publish_and_await

router = APIRouter(tags=["apps"])

TOPIC = "commands.tools"


@router.get("/apps")
async def list_apps(
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(TOPIC, "list_apps", {}, store, producer)


@router.post("/apps")
async def scaffold_app(
    body: ScaffoldAppRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "scaffold_app", body.model_dump(), store, producer,
        app_name=body.name,
    )


@router.get("/apps/{app}/entities")
async def list_entities(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "list_entities", {"app": app}, store, producer, app_name=app,
    )


@router.post("/apps/{app}/entities")
async def add_entity(
    app: str,
    body: AddEntityRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "add_entity", {"app": app, **body.model_dump()}, store, producer,
        app_name=app,
    )


@router.delete("/apps/{app}/entities/{name}")
async def remove_entity(
    app: str,
    name: str,
    confirm: bool = Query(False, description="Must be true to confirm destructive operation"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    if not confirm:
        raise HTTPException(status_code=400, detail="Destructive operation requires confirm=true")
    return await publish_and_await(
        TOPIC, "remove_entity", {"app": app, "name": name}, store, producer,
        app_name=app,
    )


@router.post("/apps/{app}/entities/{entity}/fields")
async def add_field(
    app: str,
    entity: str,
    body: AddFieldRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "add_field", {"app": app, "entity": entity, **body.model_dump()},
        store, producer, app_name=app,
    )


@router.delete("/apps/{app}/entities/{entity}/fields/{name}")
async def remove_field(
    app: str,
    entity: str,
    name: str,
    confirm: bool = Query(False, description="Must be true to confirm destructive operation"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    if not confirm:
        raise HTTPException(status_code=400, detail="Destructive operation requires confirm=true")
    return await publish_and_await(
        TOPIC, "remove_field", {"app": app, "entity": entity, "name": name},
        store, producer, app_name=app,
    )


@router.put("/apps/{app}/entities/{entity}/fields/{name}")
async def modify_field(
    app: str,
    entity: str,
    name: str,
    body: ModifyFieldRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "modify_field",
        {"app": app, "entity": entity, "name": name, **body.model_dump()},
        store, producer, app_name=app,
    )


@router.post("/apps/{app}/entities/{entity}/endpoints")
async def add_endpoint(
    app: str,
    entity: str,
    body: AddEndpointRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "add_endpoint",
        {"app": app, "entity": entity, **body.model_dump()},
        store, producer, app_name=app,
    )


@router.delete("/apps/{app}/entities/{entity}/endpoints/{name}")
async def remove_endpoint(
    app: str,
    entity: str,
    name: str,
    confirm: bool = Query(False, description="Must be true to confirm destructive operation"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    if not confirm:
        raise HTTPException(status_code=400, detail="Destructive operation requires confirm=true")
    return await publish_and_await(
        TOPIC, "remove_endpoint",
        {"app": app, "entity": entity, "name": name},
        store, producer, app_name=app,
    )


@router.post("/apps/{app}/entities/{entity}/queries")
async def add_query(
    app: str,
    entity: str,
    body: AddQueryRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "add_query",
        {"app": app, "entity": entity, **body.model_dump()},
        store, producer, app_name=app,
    )


@router.delete("/apps/{app}/entities/{entity}/queries/{name}")
async def remove_query(
    app: str,
    entity: str,
    name: str,
    confirm: bool = Query(False, description="Must be true to confirm destructive operation"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    if not confirm:
        raise HTTPException(status_code=400, detail="Destructive operation requires confirm=true")
    return await publish_and_await(
        TOPIC, "remove_query",
        {"app": app, "entity": entity, "name": name},
        store, producer, app_name=app,
    )


@router.post("/apps/{app}/entities/{entity}/relationships")
async def add_relationship(
    app: str,
    entity: str,
    body: AddRelationshipRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "add_relationship",
        {"app": app, "entity": entity, **body.model_dump()},
        store, producer, app_name=app,
    )


@router.delete("/apps/{app}/entities/{entity}/relationships/{name}")
async def remove_relationship(
    app: str,
    entity: str,
    name: str,
    confirm: bool = Query(False, description="Must be true to confirm destructive operation"),
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    if not confirm:
        raise HTTPException(status_code=400, detail="Destructive operation requires confirm=true")
    return await publish_and_await(
        TOPIC, "remove_relationship",
        {"app": app, "entity": entity, "name": name},
        store, producer, app_name=app,
    )


@router.get("/apps/{app}/status")
async def app_status(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "app_status", {"app": app}, store, producer, app_name=app,
    )


@router.put("/apps/{app}/bulk")
async def bulk_update(
    app: str,
    body: BulkUpdateRequest,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "bulk_update", {"app": app, **body.model_dump()},
        store, producer, app_name=app,
    )


@router.get("/apps/{app}/describe")
async def describe_app(
    app: str,
    store=Depends(get_correlation_store),
    producer=Depends(get_producer),
):
    return await publish_and_await(
        TOPIC, "describe_app", {"app": app}, store, producer, app_name=app,
    )
