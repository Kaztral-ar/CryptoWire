"""Encrypted Binance Square credential storage.

Only the Binance Square publishing adapter should import load_api_key().
The Discord command imports only save_api_key(), so it cannot read credentials.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from config import Settings


def _fernet(settings: Settings) -> Fernet:
    key = settings.cryptowire_secret_key.strip()
    if not key:
        raise RuntimeError(
            "CRYPTOWIRE_SECRET_KEY is not configured; generate a Fernet key "
            "and add it to the hosting provider's environment secrets."
        )
    try:
        return Fernet(key.encode("utf-8"))
    except (ValueError, TypeError) as exc:
        raise RuntimeError("CRYPTOWIRE_SECRET_KEY is not a valid Fernet key.") from exc


def save_api_key(settings: Settings, api_key: str) -> None:
    """Encrypt and atomically save an API key without returning its value."""
    normalized = api_key.strip()
    if not normalized:
        raise ValueError("The API key cannot be empty.")

    destination = Path(settings.binance_square_secret_file)
    encrypted = _fernet(settings).encrypt(normalized.encode("utf-8"))
    destination.parent.mkdir(parents=True, exist_ok=True)

    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=".binance-square-", suffix=".tmp", dir=str(destination.parent)
    )
    try:
        if hasattr(os, "fchmod"):
            os.fchmod(file_descriptor, 0o600)
        with os.fdopen(file_descriptor, "wb") as temporary_file:
            temporary_file.write(encrypted)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_name, destination)
        try:
            os.chmod(destination, 0o600)
        except OSError:
            # The encrypted file remains protected by the separately held key.
            pass
    except Exception:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise


def load_api_key(settings: Settings) -> str:
    """Decrypt the stored key. Import this only from the publishing adapter."""
    destination = Path(settings.binance_square_secret_file)
    if not destination.is_file():
        # Backward-compatible environment configuration for hosted deployments.
        return settings.binance_square_openapi_key.strip()

    try:
        encrypted = destination.read_bytes()
        return _fernet(settings).decrypt(encrypted).decode("utf-8")
    except InvalidToken as exc:
        raise RuntimeError(
            "Stored Binance Square credential cannot be decrypted. "
            "Check that CRYPTOWIRE_SECRET_KEY matches the key used when it was saved."
        ) from exc
