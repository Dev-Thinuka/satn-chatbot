"""
DB-level security helpers.

Right now this module is a placeholder for future row-level security,
encryption helpers, or tenant-aware filters on queries.
"""

from sqlalchemy.orm import Query


def apply_tenant_filter(query: Query, tenant_id: int | None) -> Query:
    """
    Example hook for multi-tenant filtering.
    Currently a no-op; extend as needed.
    """
    # Implement row-level filtering here if you add tenant_id columns later.
    return query
