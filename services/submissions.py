"""Shared submission intake used by every chat platform."""

from __future__ import annotations

import logging

from bot.permissions import can_submit

log = logging.getLogger("cryptowire.submissions")


def process_submission(
    *,
    platform: str,
    user_id: int,
    submission_id: str,
    attachment_count: int,
    admins: set[int],
    allowed_submitters: set[int],
) -> bool:
    """Authorize and register an intake event without persisting its content yet.

    Both platform adapters call this function so authorization and intake logging
    stay consistent. Draft persistence is intentionally a later implementation stage.
    """
    if not can_submit(user_id, admins, allowed_submitters):
        log.warning("Rejected %s submission from unauthorized user ID %s", platform, user_id)
        return False

    log.info(
        "Authorized submission received: platform=%s user_id=%s submission_id=%s attachments=%s",
        platform,
        user_id,
        submission_id,
        attachment_count,
    )
    return True
