from __future__ import annotations

import pytest
from cryptography.fernet import Fernet

from config import Settings
from integrations.binance_square.credentials import load_api_key, save_api_key


def make_settings(tmp_path, key: str | None = None) -> Settings:
    return Settings(
        cryptowire_secret_key=key or Fernet.generate_key().decode("ascii"),
        binance_square_secret_file=str(tmp_path / "storage" / "binance_square_api_key.enc"),
        binance_square_openapi_key="",
    )


def test_api_key_is_encrypted_at_rest_and_can_be_loaded(tmp_path) -> None:
    settings = make_settings(tmp_path)
    secret = "test-binance-square-key-do-not-use"

    save_api_key(settings, secret)

    encrypted = (tmp_path / "storage" / "binance_square_api_key.enc").read_bytes()
    assert secret.encode() not in encrypted
    assert load_api_key(settings) == secret


def test_api_key_can_be_replaced(tmp_path) -> None:
    settings = make_settings(tmp_path)

    save_api_key(settings, "old-test-key")
    save_api_key(settings, "new-test-key")

    assert load_api_key(settings) == "new-test-key"


def test_empty_api_key_is_rejected(tmp_path) -> None:
    settings = make_settings(tmp_path)

    with pytest.raises(ValueError, match="cannot be empty"):
        save_api_key(settings, "   ")


def test_missing_encryption_key_is_rejected(tmp_path) -> None:
    settings = make_settings(tmp_path, key="")

    with pytest.raises(RuntimeError, match="CRYPTOWIRE_SECRET_KEY"):
        save_api_key(settings, "some-test-key")


def test_wrong_encryption_key_fails_closed(tmp_path) -> None:
    settings = make_settings(tmp_path)
    save_api_key(settings, "test-api-key")

    wrong_settings = make_settings(tmp_path, key=Fernet.generate_key().decode("ascii"))
    with pytest.raises(RuntimeError, match="cannot be decrypted"):
        load_api_key(wrong_settings)


def test_environment_fallback_is_used_only_when_encrypted_file_missing(tmp_path) -> None:
    settings = make_settings(tmp_path)
    settings.binance_square_openapi_key = "environment-test-key"

    assert load_api_key(settings) == "environment-test-key"
