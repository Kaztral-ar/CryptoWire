<div align="center">

<img src="assets/cryptowire-banner.svg" alt="CryptoWire — one intake, two platforms, controlled publishing" width="100%"/>

[![CI](https://github.com/Kaztral-ar/CryptoWire/actions/workflows/ci.yml/badge.svg)](https://github.com/Kaztral-ar/CryptoWire/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-supported-5865F2?logo=discord&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-supported-26A5E4?logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-check%20repository-lightgrey)

**A shared submission gateway for Discord and Telegram, built for controlled Binance Square publishing.**

</div>

---

## What it does

- Receives submissions from a Discord channel and an optional Telegram bot.
- Routes both platforms through one shared intake and authorization service.
- Allows only configured admins and submitters.
- Stores Binance API credentials encrypted when configured through Discord.

> **Current stage:** Platform intake and access control are implemented. Draft storage, approval actions, and Binance Square publishing are not implemented yet. Submissions are not published automatically.

## Flow

```text
 Discord ──┐
           ├──► Shared intake ──► Authorization
 Telegram ─┘
```

## Deploy

Run CryptoWire as an **always-on Python worker** (Render Background Worker, Railway service, or a VPS). It needs a persistent process; do not deploy it as a static website or short-lived serverless function.

### 1. Create the bots

- Create a Discord application in the [Discord Developer Portal](https://discord.com/developers/applications). Enable **Message Content Intent** and invite the bot with `bot` and `applications.commands` scopes.
- Optional: create a Telegram bot with [@BotFather](https://t.me/BotFather).

### 2. Deploy the repository

For a worker service, use:

| Setting | Value |
| --- | --- |
| Repository | `Kaztral-ar/CryptoWire` |
| Runtime | Python 3.11+ |
| Build command | `pip install -r requirements.txt` |
| Start command | `python bot.py` |

### 3. Add environment variables

Set these in your hosting provider's environment/secrets settings:

| Variable | Required | Description |
| --- | :---: | --- |
| `DISCORD_BOT_TOKEN` | Yes | Discord bot token |
| `SUBMISSION_CHANNEL_ID` | Yes | Discord intake channel ID |
| `ADMIN_USER_IDS` | Yes | Comma-separated Discord admin IDs |
| `TELEGRAM_BOT_TOKEN` | No | Enables Telegram when set |
| `TELEGRAM_ADMIN_USER_IDS` | If Telegram enabled | Comma-separated Telegram admin IDs |
| `ALLOWED_SUBMITTER_IDS` | No | Additional Discord submitter IDs |
| `TELEGRAM_ALLOWED_SUBMITTER_IDS` | No | Additional Telegram submitter IDs |
| `CRYPTOWIRE_SECRET_KEY` | For API key setup | Fernet key for encrypted credential storage |

Generate the encryption key when needed:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Keep tokens and encryption keys out of Git. If you use `/set_api_key`, attach persistent storage for `storage/binance_square_api_key.enc` and keep `CRYPTOWIRE_SECRET_KEY` separately in the host's secret settings.

### 4. Start

Deploy/restart the worker. In Telegram, open your bot and send `/start`. In Discord, send a test message in the configured submission channel.

## Run locally

```bash
git clone https://github.com/Kaztral-ar/CryptoWire.git
cd CryptoWire
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env            # Add your tokens and IDs
python bot.py
```

## Project status

| Feature | Status |
| --- | --- |
| Discord + Telegram intake | <span>Implemented</span> |
| Shared authorization | Implemented |
| Encrypted API-key setup | Implemented |
| Persistent drafts and media | Planned |
| Preview + approve/reject | Planned |
| Binance Square publishing | Planned |

## Development

```bash
pytest -q
```

Contributions and bug reports are welcome. See [Issues](https://github.com/Kaztral-ar/CryptoWire/issues).

---

<div align="center">

**CryptoWire** · Receive first. Review next. Publish only when approved.

</div>
