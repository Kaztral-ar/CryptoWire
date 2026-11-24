from bot.permissions import can_submit, is_admin


def test_admin_can_submit_without_submitter_allowlist() -> None:
    assert can_submit(10, {10}, set()) is True


def test_allowlisted_user_can_submit() -> None:
    assert can_submit(20, {10}, {20}) is True


def test_unknown_user_is_denied_by_default() -> None:
    assert can_submit(30, {10}, {20}) is False


def test_admin_check() -> None:
    assert is_admin(10, {10}) is True
    assert is_admin(11, {10}) is False
