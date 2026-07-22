"""Server-side session lifecycle primitives for the local training lab.

The production token generator is ``secrets.token_bytes``.  It is backed by the
operating system's cryptographically secure random source.  Thirty-two random
bytes provide 256 bits of entropy before hexadecimal encoding.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import secrets
import time
from typing import Callable, Optional


Clock = Callable[[], float]
TokenFactory = Callable[[], str]


@dataclass
class SessionRecord:
    """Sensitive session state that exists only on the server."""

    state: str
    user_id: Optional[str]
    tenant_id: Optional[str]
    role: Optional[str]
    auth_level: str
    issued_at: float
    authenticated_at: Optional[float]
    last_seen_at: float
    absolute_expires_at: float
    revoked_at: Optional[float] = None
    revocation_reason: Optional[str] = None


class FakeClock:
    """Injectable deterministic clock used by tests instead of real sleeps."""

    def __init__(self, initial: float = 1_000.0) -> None:
        self._now = float(initial)

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("A fake clock cannot move backwards")
        self._now += float(seconds)


class SessionManager:
    """Issue, rotate, validate, expire, and revoke opaque session IDs."""

    TOKEN_BYTES = 32
    TOKEN_ENTROPY_BITS = TOKEN_BYTES * 8

    def __init__(
        self,
        *,
        idle_timeout: float = 300.0,
        absolute_timeout: float = 1_800.0,
        clock: Clock = time.time,
        token_factory: Optional[TokenFactory] = None,
        log_key: Optional[bytes] = None,
    ) -> None:
        if idle_timeout <= 0 or absolute_timeout <= 0:
            raise ValueError("Session timeouts must be positive")
        if idle_timeout > absolute_timeout:
            raise ValueError("Idle timeout cannot exceed absolute timeout")

        self.idle_timeout = float(idle_timeout)
        self.absolute_timeout = float(absolute_timeout)
        self.clock = clock
        self._token_factory = token_factory or self._csprng_token
        self._log_key = log_key or secrets.token_bytes(32)
        self._sessions: dict[str, SessionRecord] = {}
        self._events: list[str] = []

    @classmethod
    def _csprng_token(cls) -> str:
        """Return 32 CSPRNG bytes encoded as 64 hexadecimal characters."""

        return secrets.token_bytes(cls.TOKEN_BYTES).hex()

    def fingerprint(self, token: str) -> str:
        """Return a keyed, non-reversible correlation value for safe logging."""

        digest = hmac.new(
            self._log_key,
            token.encode("utf-8", errors="replace"),
            hashlib.sha256,
        ).hexdigest()
        return digest[:16]

    def _log(self, event: str, token: str, detail: str = "") -> None:
        suffix = f" {detail}" if detail else ""
        self._events.append(
            f"event={event} session_fp={self.fingerprint(token)}{suffix}"
        )

    def log_events(self) -> tuple[str, ...]:
        return tuple(self._events)

    def _new_token(self) -> str:
        # A collision is extraordinarily unlikely, but uniqueness is still
        # enforced against the server-side store rather than assumed.
        for _ in range(100):
            token = self._token_factory()
            if not isinstance(token, str) or not token:
                raise ValueError("Token factory must return a non-empty string")
            if token not in self._sessions:
                return token
        raise RuntimeError("Token generator repeatedly produced duplicates")

    def _issue(
        self,
        *,
        state: str,
        user_id: Optional[str],
        tenant_id: Optional[str],
        role: Optional[str],
        auth_level: str,
        authenticated_at: Optional[float] = None,
        absolute_expires_at: Optional[float] = None,
    ) -> str:
        now = self.clock()
        token = self._new_token()
        record = SessionRecord(
            state=state,
            user_id=user_id,
            tenant_id=tenant_id,
            role=role,
            auth_level=auth_level,
            issued_at=now,
            authenticated_at=authenticated_at,
            last_seen_at=now,
            absolute_expires_at=(
                absolute_expires_at
                if absolute_expires_at is not None
                else now + self.absolute_timeout
            ),
        )
        self._sessions[token] = record
        self._log("issued", token, f"state={state}")
        return token

    def start_anonymous(self, presented_token: Optional[str] = None) -> str:
        """Issue a pre-login token, replacing any token the client supplied."""

        if presented_token:
            self.revoke(presented_token, reason="prelogin_replaced")
        return self._issue(
            state="anonymous",
            user_id=None,
            tenant_id=None,
            role=None,
            auth_level="anonymous",
        )

    def authenticate(
        self,
        *,
        presented_token: Optional[str],
        user_id: str,
        tenant_id: str,
        role: str,
    ) -> str:
        """Replace the pre-login token and create an authenticated session."""

        if presented_token:
            self.revoke(presented_token, reason="login_rotation")
        now = self.clock()
        return self._issue(
            state="authenticated",
            user_id=user_id,
            tenant_id=tenant_id,
            role=role,
            auth_level="standard",
            authenticated_at=now,
        )

    def rotate_for_privilege_change(
        self,
        token: str,
        *,
        trusted_role: Optional[str] = None,
        new_auth_level: str = "elevated",
    ) -> Optional[str]:
        """Revoke the old ID and issue a new ID after a trusted privilege change.

        Rotation does not extend the original absolute lifetime.
        """

        record = self.resolve(token, touch=False)
        if record is None or record.state != "authenticated":
            return None

        self.revoke(token, reason="privilege_rotation")
        return self._issue(
            state="authenticated",
            user_id=record.user_id,
            tenant_id=record.tenant_id,
            role=trusted_role if trusted_role is not None else record.role,
            auth_level=new_auth_level,
            authenticated_at=record.authenticated_at,
            absolute_expires_at=record.absolute_expires_at,
        )

    def resolve(self, token: Optional[str], *, touch: bool = True) -> Optional[SessionRecord]:
        """Resolve an active token and enforce idle and absolute expiration."""

        if not token:
            return None
        record = self._sessions.get(token)
        if record is None:
            self._log("rejected_unknown", token)
            return None
        if record.state in {"revoked", "expired"}:
            self._log("rejected_inactive", token, f"state={record.state}")
            return None

        now = self.clock()
        if now >= record.absolute_expires_at:
            record.state = "expired"
            record.revoked_at = now
            record.revocation_reason = "absolute_timeout"
            self._log("expired", token, "reason=absolute_timeout")
            return None
        if now - record.last_seen_at >= self.idle_timeout:
            record.state = "expired"
            record.revoked_at = now
            record.revocation_reason = "idle_timeout"
            self._log("expired", token, "reason=idle_timeout")
            return None

        if touch:
            record.last_seen_at = now
        return record

    def revoke(self, token: Optional[str], *, reason: str = "logout") -> bool:
        """Invalidate a token in server-side state."""

        if not token:
            return False
        record = self._sessions.get(token)
        if record is None:
            self._log("revocation_unknown", token, f"reason={reason}")
            return False
        if record.state in {"revoked", "expired"}:
            return False

        record.state = "revoked"
        record.revoked_at = self.clock()
        record.revocation_reason = reason
        self._log("revoked", token, f"reason={reason}")
        return True

    def safe_snapshot(self, token: str) -> Optional[dict[str, object]]:
        """Expose safe server-side metadata for tests; never return the token."""

        record = self._sessions.get(token)
        if record is None:
            return None
        return {
            "state": record.state,
            "user_id": record.user_id,
            "tenant_id": record.tenant_id,
            "role": record.role,
            "auth_level": record.auth_level,
            "issued_at": record.issued_at,
            "last_seen_at": record.last_seen_at,
            "absolute_expires_at": record.absolute_expires_at,
            "revocation_reason": record.revocation_reason,
            "session_fp": self.fingerprint(token),
        }
