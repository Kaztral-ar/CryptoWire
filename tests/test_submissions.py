from services.submissions import Submission, process_submission


def test_authorized_discord_submission_is_accepted(caplog) -> None:
    submission = Submission(
        platform="discord",
        user_id=100,
        submission_id="discord-message-1",
        content="hello from Discord",
        attachment_count=2,
    )
    assert process_submission(
        submission, admins={100}, allowed_submitters=set()
    ) is True
    assert "platform=discord" in caplog.text
    assert "hello from Discord" not in caplog.text


def test_authorized_telegram_submitter_is_accepted(caplog) -> None:
    submission = Submission(
        platform="telegram",
        user_id=200,
        submission_id="telegram-message-1",
        content="hello from Telegram",
        attachment_count=1,
    )
    assert process_submission(
        submission, admins={100}, allowed_submitters={200}
    ) is True
    assert "platform=telegram" in caplog.text
    assert "hello from Telegram" not in caplog.text


def test_unauthorized_submission_is_rejected() -> None:
    submission = Submission(
        platform="telegram",
        user_id=300,
        submission_id="telegram-message-2",
        content="not authorized",
        attachment_count=0,
    )
    assert process_submission(
        submission, admins={100}, allowed_submitters={200}
    ) is False
