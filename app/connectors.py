"""Vendor-neutral contract. No vendor adapters or credentials ship in this demo."""
from dataclasses import dataclass
from typing import Protocol, Optional, Sequence

@dataclass(frozen=True)
class AccessSnapshot:
    allow_principals: Sequence[str]
    deny_principals: Sequence[str]
    checked_at: str
    valid_until: str
    authoritative: bool

@dataclass(frozen=True)
class SourceRecord:
    tenant_id: str
    connection_id: str
    external_id: str
    revision: str
    title: str
    body: str
    source_url: str
    acl: AccessSnapshot
    deleted: bool = False

@dataclass(frozen=True)
class ChangePage:
    records: Sequence[SourceRecord]
    next_cursor: Optional[str]

class Connector(Protocol):
    """Implement per provider; validate capabilities before enabling ingestion.

    Context/credentials are provisioned per tenant by the server, never caller IDs.
    A checkpoint advances only after records + tombstones commit successfully.
    """
    def changes(self, cursor: Optional[str]) -> ChangePage: ...
    def current_access(self, external_id: str) -> AccessSnapshot: ...
    def fetch(self, external_id: str) -> SourceRecord: ...
    def revoke(self) -> None: ...
