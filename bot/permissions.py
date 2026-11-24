"""Default-deny Discord authorization helpers."""

from __future__ import annotations


def is_admin(user_id: int, admin_ids: set[int]) -> bool:
    return user_id in admin_ids


def can_submit(user_id: int, admin_ids: set[int], submitter_ids: set[int]) -> bool:
    """Admins may submit; other users must be explicitly allowlisted."""
    return is_admin(user_id, admin_ids) or user_id in submitter_ids
