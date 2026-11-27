"""Shared submission intake used by every chat platform."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from bot.permissions import can_submit

log = logging.getLogger("cryptowire.submissions")


@dataclass(frozen=True, slots=True)
class Submission:
    platform: str
    user_id: int
    submission_id: str
    content: str
    attachment_count: int


def process_submission(
    submission: Submission,
    *,
    admins: set[int],
    allowed_submitters: set[int],
) -> bool:
    """Authorize and pass a normalized submission through shared intake.

    Content is passed to this common boundary but is not persisted in Stage 2.
    Logs intentionally contain metadata only, never submitted text or captions.
    """
    if not can_submit(submission.user_id, admins, allowed_submitters):
        log.warning(
            "Rejected %s submission from unauthorized user ID %s",
            submission.platform,
            submission.user_id,
        )
        return False

    log.info(
        "Authorized submission received: platform=%s user_id=%s submission_id=%s attachments=%s",
        submission.platform,
        submission.user_id,
        submission.submission_id,
        submission.attachment_count,
    )
    return True
