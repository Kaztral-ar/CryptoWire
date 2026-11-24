# CryptoWire

A Python Discord-to-Binance Square publishing assistant.

CryptoWire receives content from an authorized Discord server, prepares a draft, and requires an administrator's explicit approval before attempting publication through Binance's official Square publishing integration.

> **Current status:** Stage 2 Discord foundation implemented. Draft processing, approval, and Binance publishing are not implemented yet.

## Current Stage 2 features

- Discord client and application-command synchronization.
- `/help` and `/status` slash commands.
- Default-deny submission permissions: administrators and explicitly allowlisted users only.
- Monitoring of one configured submission channel.
- Acknowledgement reaction for authorized submissions.
- Logging of message IDs and attachment counts without logging message contents.
- Startup configuration checks and graceful shutdown.

## Planned workflow

1. An authorized user submits text and supported media in a configured Discord channel.
2. CryptoWire validates permissions and content, then creates a draft.
3. The bot posts a preview with approval, rejection, and edit controls.
4. An authorized administrator approves the exact draft version.
5. A publishing worker hands the approved draft to the Binance Square adapter.
6. The result and audit event are stored.

## Stack

- Python 3.11+
- discord.py
- SQLAlchemy + SQLite (planned for persistence stages)
- Pydantic Settings
- pytest
- Official Binance Square publishing integration (Node.js runtime required by the official scripts; invoked through a Python adapter)

## Repository layout

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
│   └── status.py
├── core/                       # Later stages
├── integrations/binance_square/ # Later stages
├── database/                   # Later stages
├── utils/                      # Later stages
├── tests/
└── docs/
```

## Setup

1. Install Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and fill in the required Discord configuration.
5. In the Discord Developer Portal, enable **Message Content Intent** under Bot → Privileged Gateway Intents.
6. Invite the bot with the `bot` and `applications.commands` scopes. Grant only View Channels, Send Messages, Read Message History, Add Reactions, and Embed Links where needed.
7. Run `python bot.py`.

## Required configuration

- `DISCORD_BOT_TOKEN`: bot token from the Discord Developer Portal.
- `SUBMISSION_CHANNEL_ID`: channel where authorized users submit content.
- `ADMIN_USER_IDS`: comma-separated numeric Discord user IDs; at least one is required.

Optional:
- `DISCORD_GUILD_ID`: enables fast guild-scoped slash-command sync during development. If omitted, commands sync globally and may take time to appear.
- `ALLOWED_SUBMITTER_IDS`: comma-separated IDs allowed to submit in addition to admins. Empty means admins only.
- `APPROVAL_CHANNEL_ID`: reserved for the approval workflow stage.

Never commit `.env`, Discord bot tokens, Binance credentials, or user media.

## Stage 2 boundaries

Authorized messages in the submission channel are acknowledged with a 📥 reaction and logged by message ID and attachment count. Unauthorized messages receive a brief notice. Stage 2 does not save message content, download media, create drafts, approve posts, or publish to Binance.

## Tests

```bash
pytest -q
```

## Security principles

- Default-deny access: only configured submitters and admins may submit.
- Only configured administrators may approve or reject drafts in the future approval stage.
- Approval will be bound to a draft version; editing invalidates prior approval.
- Never publish automatically on receipt.
- Keep credentials out of source control and logs.
- Validate attachment size, MIME type, and supported publishing formats.
- Record publishing attempts and administrative actions.
- Do not retry ambiguous publishing outcomes blindly; reconcile first to avoid duplicate posts.

## Binance publishing integration

The publishing adapter will be implemented against Binance's official Square publishing integration. Verify current API access, account eligibility, media limits, and credential requirements before enabling production publishing.

- [Official Binance Square publishing integration](https://github.com/binance/binance-skills-hub/tree/main/skills/binance/square-post)
- [Binance Square Creator Center](https://www.binance.com/square/creator-center/home)

CryptoWire does not use trading permissions and should never request withdrawal permissions.

## Development status

- [x] Stage 1: architecture and repository scaffold
- [x] Stage 2: Discord bot foundation and access control
- [ ] Stage 3: submission intake, attachment handling, and drafts
- [ ] Stage 4: approval workflow
- [ ] Stage 5: Binance Square publishing adapter
- [ ] Stage 6: persistent database and audit history
- [ ] Stage 7: integration tests and deployment

## License

License to be selected before public release.
