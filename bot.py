"""CryptoWire application entry point.

The Discord client and workflow handlers will be added in Stage 2.
"""

from __future__ import annotations

import logging

from config import get_settings


def main() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("cryptowire").info(
        "CryptoWire scaffold loaded. Discord runtime is not implemented yet."
    )


if __name__ == "__main__":
    main()
