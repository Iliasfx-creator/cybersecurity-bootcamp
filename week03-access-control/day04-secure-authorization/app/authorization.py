from __future__ import annotations

from enum import Enum
from typing import Mapping


class Action(str, Enum):
    LIST_DOCUMENTS = "documents:list"
    READ_DOCUMENT = "document:read"
    UPDATE_DOCUMENT = "document:update"
    CHANGE_USER_ROLE = "user-role:change"


def is_authorized(
    actor: Mapping[str, object] | None,
    action: Action | str,
    resource: Mapping[str, object] | None = None,
) -> bool:
    """Return True only for permissions explicitly granted by policy."""
    if actor is None:
        return False

    username = actor.get("username")
    role = actor.get("role")

    if not isinstance(username, str):
        return False

    if role not in {"user", "admin"}:
        return False

    if action == Action.LIST_DOCUMENTS:
        return True

    if action in {
        Action.READ_DOCUMENT,
        Action.UPDATE_DOCUMENT,
    }:
        if resource is None:
            return False

        return (
            role == "admin"
            or resource.get("owner") == username
        )

    if action == Action.CHANGE_USER_ROLE:
        return role == "admin"

    return False
