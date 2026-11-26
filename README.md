# CryptoWire

<p align="center">
  <strong>Discord → Review → Binance Square</strong><br/>
  A controlled publishing assistant for Binance Square, built with Python and Discord.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+"/>&nbsp;
  <img src="https://img.shields.io/badge/Discord-discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="discord.py"/>&nbsp;
  <img src="https://img.shields.io/badge/Storage-SQLite%20planned-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite planned"/>
</p>

CryptoWire is a Discord-based workflow for preparing content for Binance Square. It is designed around one important rule: **receiving a submission must never publish it automatically**. Content should be reviewed and explicitly approved by an authorized administrator before a publishing integration is allowed to send it.

> **Development status:** The Discord foundation, access controls, and encrypted API-key configuration command are implemented. Draft creation, interactive approval, and Binance Square publishing are not implemented yet.

---

## At a glance

| Area | Current state |
| --- | --- |
| Discord bot foundation | Implemented |
| `/help` and `/status` | Implemented |
| Submission-channel access control | Implemented |
| Admin-only `/set_api_key` | Implemented |
| Encrypted API-key storage | Implemented |
| Draft creation and media handling | Planned |
| Preview and approval controls | Planned |
| Binance Square publishing | Planned |

## How CryptoWire is intended to work

```text
Authorized Discord submission
             │
             ▼
      Content validation
             │
             ▼
       Draft + preview
             │
             ▼
    Administrator review
        │         │
      Reject    Approve
                  │
                  ▼
       Binance Square adapter
                  │
                  ▼
        Publish result + audit
```

The diagram describes the target workflow, not a claim that every stage is already available.

## Implemented features

- **Discord application commands:** command synchronization plus `/help` and `/status`.
- **Restricted submission intake:** the bot monitors the configured submission channel and accepts messages only from administrators or explicitly allowlisted submitters.
- **Administrator-only credential setup:** `/set_api_key` opens a private Discord modal for a configured administrator.
- **Encrypted credential storage:** the submitted key is encrypted with Fernet before it is written to the configured local file.
- **No credential echo:** the bot does not include the API key in its confirmation response or application logs.
- **Acknowledgement:** authorized submissions receive a 📥 reaction.

## Quick start

### 1. Requirements

- Python 3.11 or newer
- A Discord application and bot
- A Discord server where you can configure channel and administrator IDs
- A persistent writable storage location for the encrypted credential file

### 2. Install

```bash
git clone https://github.com/Kaztral-ar/CryptoWire.git
cd CryptoWire

python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\\Scripts\\Activate.ps1

pip install -r requirements.txt
```

### 3. Configure environment

Copy the example file:

```bash
cp .env.example .env
```

On Windows, copy `.env.example` to `.env` manually or use:

```powershell
Copy-Item .env.example .env
```

Set the Discord bot token, submission channel ID, and at least one administrator user ID in `.env`.

| Variable | Required | Purpose |
| --- | --- | --- |
| `DISCORD_BOT_TOKEN` | Yes | Discord bot token |
| `SUBMISSION_CHANNEL_ID` | Yes | Channel monitored for submissions |
| `ADMIN_USER_IDS` | Yes | Comma-separated Discord administrator IDs |
| `CRYPTOWIRE_SECRET_KEY` | For `/set_api_key` | Fernet encryption key, stored separately from encrypted credential |
| `DISCORD_GUILD_ID` | No | Guild-scoped command sync for development |
| `ALLOWED_SUBMITTER_IDS` | No | Additional comma-separated submitter IDs |
| `APPROVAL_CHANNEL_ID` | No | Reserved for the planned approval workflow |
| `BINANCE_SQUARE_SECRET_FILE` | No | Encrypted credential path; defaults to `storage/binance_square_api_key.enc` |
| `BINANCE_SQUARE_OPENAPI_KEY` | No | Legacy environment-based credential fallback for the future adapter |
| `DATABASE_URL` | No | Reserved application database setting |
| `LOG_LEVEL` | No | Logging level; defaults to `INFO` |

### 4. Generate the encryption key

Generate a Fernet key locally:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Put the generated value in `CRYPTOWIRE_SECRET_KEY`. For deployment, configure it as a secret/environment variable in your hosting provider rather than committing it to the repository.

**Keep this encryption key safe and backed up.** The encrypted Binance credential cannot be recovered if the matching Fernet key is lost. The encryption key and encrypted credential file must be retained separately.

### 5. Configure Discord

In the Discord Developer Portal:

1. Open your application and its **Bot** settings.
2. Enable **Message Content Intent**.
3. Invite the bot using the `bot` and `applications.commands` scopes.
4. Grant only the channel permissions it needs, including viewing the submission channel, reading message history, sending messages, and adding reactions.

### 6. Start the bot

```bash
python bot.py
```

## Configure the Binance Square API key

Once the bot is running and `CRYPTOWIRE_SECRET_KEY` is configured:

1. A configured administrator runs `/set_api_key` in Discord.
2. CryptoWire opens a private interaction modal.
3. The administrator enters the Binance Square API key.
4. The bot encrypts the key and writes it to `BINANCE_SQUARE_SECRET_FILE`.
5. The bot returns a private success or failure message without displaying the key.

The command checks administrator authorization both when it is opened and when the modal is submitted. The command handler has write-only access: it can store the credential but cannot retrieve it. The future publishing adapter is intended to be the only component that reads it.

**Discord modal limitation:** Discord's text input is not a password field. The key can be visible on the administrator's screen while being entered. Use this command only in a trusted server and device.

To replace a key, run `/set_api_key` again with the new credential. Revoke credentials that have been exposed.

## Security model

CryptoWire is being designed with credential isolation and explicit human approval as core requirements.

- Never commit `.env`, bot tokens, Binance API keys, Fernet keys, or runtime credential files.
- Keep `CRYPTOWIRE_SECRET_KEY` in the hosting provider's secret manager/environment, separate from the encrypted credential file.
- Restrict `/set_api_key` to the IDs configured in `ADMIN_USER_IDS`.
- Do not log credentials or include them in Discord messages.
- Do not grant trading or withdrawal permissions to a credential intended for Square publishing.
- Do not publish automatically when a Discord message is received.
- Bind future approval to the exact draft version; edits must invalidate prior approval.
- Treat ambiguous publishing outcomes carefully. Reconcile before retrying to avoid duplicate posts.
- Use persistent storage for the encrypted credential file in deployments where the filesystem is ephemeral.

**Credential boundary:** `commands/set_api_key.py` imports the write operation only. The decryption helper is isolated in `integrations/binance_square/credentials.py` for use by the future publishing adapter.

## Project structure

```text
CryptoWire/
├── bot.py
├── config.py
├── requirements.txt
├── .env.example
├── bot/
│   ├── client.py
│   └── permissions.py
├── commands/
│   ├── help.py
│   ├── status.py
│   └── set_api_key.py
├── integrations/
│   └── binance_square/
│       └── credentials.py
├── tests/
└── docs/
```

## Roadmap

- [x] Stage 1 — Architecture and repository scaffold
- [x] Stage 2 — Discord client, commands, and access control
- [x] Administrator-only encrypted Binance API-key setup
- [ ] Stage 3 — Submission intake, attachment validation, draft storage, and Discord preview
- [ ] Stage 4 — Administrator approval/rejection workflow and version-bound approvals
- [ ] Stage 5 — Official Binance Square publishing adapter
- [ ] Stage 6 — Persistent audit history and publishing-result tracking
- [ ] Stage 7 — Integration tests, deployment, and operational hardening

## Tests

Run the current test suite from the repository root:

```bash
pytest -q
```

Live Discord interactions and real Binance Square publishing have not been verified. Publishing remains disabled until the adapter and approval workflow are implemented and tested.

## Binance Square resources

- [Binance Square Creator Center](https://www.binance.com/square/creator-center/home)
- [Official Binance Square publishing integration](https://github.com/binance/binance-skills-hub/tree/main/skills/binance/square-post)

Before enabling publication, verify current Binance account eligibility, API access requirements, supported content formats, and publishing limits against Binance's official documentation.


## ☕ Support

If you find this project useful, you can support its development with a coffee.

<a href="https://buymeacoffee.com/k4tral" target="_blank">
  <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support%20my%20work-yellow?style=for-the-badge&logo=buymeacoffee&logoColor=white" alt="Buy Me a Coffee" />
</a>

<p align="center">
  Built for controlled publishing. <strong>Review first. Publish only after approval.</strong>
</p>
