from __future__ import annotations

from enum import Enum
from typing import Mapping


KNOWN_TENANTS = {"alpha", "beta"}

KNOWN_ROLES = {
    "user",
    "tenant_admin",
    "support_admin",
}


class Action(str, Enum):
    LIST_DOCUMENTS = "documents:list"
    READ_DOCUMENT = "document:read"
    UPDATE_DOCUMENT = "document:update"
    EXPORT_ORGANIZATION = "organization:export"
    RUN_SUPPORT_OPERATION = "support:operate"
    READ_AUDIT_LOG = "audit:read"


def valid_actor(actor: Mapping[str, object] | None) -> bool:
    if actor is None:
        return False

    username = actor.get("username")
    role = actor.get("role")
    tenant_id = actor.get("tenant_id")

    if not isinstance(username, str) or not username:
        return False

    if role not in KNOWN_ROLES:
        return False

    if role == "support_admin":
        return tenant_id is None

    return tenant_id in KNOWN_TENANTS


def authorize(
    actor: Mapping[str, object] | None,
    action: Action | str,
    resource: Mapping[str, object] | None = None,
    target_tenant: str | None = None,
) -> bool:
    """Return True only when the central policy explicitly grants access."""

    if not valid_actor(actor):
        return False

    try:
        requested_action = Action(action)
    except (TypeError, ValueError):
        return False

    role = actor["role"]
    actor_tenant = actor["tenant_id"]
    username = actor["username"]

    if requested_action == Action.LIST_DOCUMENTS:
        return role in {"user", "tenant_admin"}

    if requested_action in {
        Action.READ_DOCUMENT,
        Action.UPDATE_DOCUMENT,
    }:
        if resource is None:
            return False

        resource_tenant = resource.get("tenant_id")
        owner_id = resource.get("owner_id")

        if resource_tenant not in KNOWN_TENANTS:
            return False

        if not isinstance(owner_id, str):
            return False

        if role == "user":
            return (
                actor_tenant == resource_tenant
                and username == owner_id
            )

        if role == "tenant_admin":
            return actor_tenant == resource_tenant

        return False

    if requested_action == Action.EXPORT_ORGANIZATION:
        return (
            target_tenant in KNOWN_TENANTS
            and role == "tenant_admin"
            and actor_tenant == target_tenant
        )

    if requested_action == Action.RUN_SUPPORT_OPERATION:
        return (
            target_tenant in KNOWN_TENANTS
            and role == "support_admin"
        )

    if requested_action == Action.READ_AUDIT_LOG:
        return role == "support_admin"

    return False
