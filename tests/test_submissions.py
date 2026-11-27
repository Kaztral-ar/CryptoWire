from services.submissions import process_submission


def test_authorized_discord_submission_is_accepted(caplog) -> None:
    assert process_submission(
        platform="discord",
        user_id=100,
        submission_id="discord-message-1",
        attachment_count=2,
        admins={100},
        allowed_submitters=set(),
    ) is True
    assert "platform=discord" in caplog.text


def test_authorized_telegram_submitter_is_accepted(caplog) -> None:
    assert process_submission(
        platform="telegram",
        user_id=200,
        submission_id="telegram-message-1",
        attachment_count=1,
        admins={100},
        allowed_submitters={200},
    ) is True
    assert "platform=telegram" in caplog.text


def test_unauthorized_submission_is_rejected() -> None:
    assert process_submission(
        platform="telegram",
        user_id=300,
        submission_id="telegram-message-2",
        attachment_count=0,
        admins={100},
        allowed_submitters={200},
    ) is False
