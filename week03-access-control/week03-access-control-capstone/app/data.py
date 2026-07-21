from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone


INITIAL_USERS = {
    "alice": {
        "id": "user-alpha-alice",
        "username": "alice",
        "tenant_id": "alpha",
        "role": "user",
        "display_name": "Alice",
    },
    "bob": {
        "id": "user-beta-bob",
        "username": "bob",
        "tenant_id": "beta",
        "role": "user",
        "display_name": "Bob",
    },
    "admin_alpha": {
        "id": "user-alpha-admin",
        "username": "admin_alpha",
        "tenant_id": "alpha",
        "role": "tenant_admin",
        "display_name": "Alpha Administrator",
    },
    "support_admin": {
        "id": "user-platform-support",
        "username": "support_admin",
        "tenant_id": None,
        "role": "support_admin",
        "display_name": "Platform Support",
    },
}


INITIAL_DOCUMENTS = {
    "alpha-1001": {
        "id": "alpha-1001",
        "tenant_id": "alpha",
        "owner_id": "alice",
        "title": "Alpha project plan",
        "content": "Alpha document owned by Alice.",
        "internal_label": "alpha-confidential",
    },
    "alpha-1002": {
        "id": "alpha-1002",
        "tenant_id": "alpha",
        "owner_id": "admin_alpha",
        "title": "Alpha administration notes",
        "content": "Alpha document owned by the tenant administrator.",
        "internal_label": "alpha-restricted",
    },
    "beta-2001": {
        "id": "beta-2001",
        "tenant_id": "beta",
        "owner_id": "bob",
        "title": "Beta project plan",
        "content": "Beta document owned by Bob.",
        "internal_label": "beta-confidential",
    },
    "beta-2002": {
        "id": "beta-2002",
        "tenant_id": "beta",
        "owner_id": "bob",
        "title": "Beta operational notes",
        "content": "Second Beta document owned by Bob.",
        "internal_label": "beta-restricted",
    },
}


V2_DOCUMENT_WRITE_FIELDS = frozenset({"title", "content"})

V2_DOCUMENT_RESPONSE_FIELDS = (
    "id",
    "owner_id",
    "title",
    "content",
)


USERS: dict[str, dict[str, object]] = {}
DOCUMENTS: dict[str, dict[str, object]] = {}
SESSIONS: dict[str, str] = {}
AUDIT_LOG: list[dict[str, object]] = []


def reset_state() -> None:
    USERS.clear()
    USERS.update(deepcopy(INITIAL_USERS))

    DOCUMENTS.clear()
    DOCUMENTS.update(deepcopy(INITIAL_DOCUMENTS))

    SESSIONS.clear()
    AUDIT_LOG.clear()


def public_document(document: dict[str, object]) -> dict[str, object]:
    return {
        field: document[field]
        for field in V2_DOCUMENT_RESPONSE_FIELDS
    }


def record_audit(
    actor: dict[str, object],
    action: str,
    target: str,
    outcome: str,
) -> dict[str, object]:
    event = {
        "id": f"audit-{len(AUDIT_LOG) + 1}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": actor["username"],
        "actor_role": actor["role"],
        "action": action,
        "target": target,
        "outcome": outcome,
    }

    AUDIT_LOG.append(event)
    return deepcopy(event)


reset_state()
