# CryptoWire

A Python Discord-to-Binance Square publishing assistant.

CryptoWire receives content from an authorized Discord server, prepares a draft, and requires an administrator's explicit approval before attempting publication through Binance's official Square publishing integration.

> **Status:** Initial repository scaffold. Publishing is not implemented yet.

## Planned workflow

1. An authorized user submits text and supported media in a configured Discord channel.
2. CryptoWire validates permissions and content, then creates a draft.
3. The bot posts a preview with approval, rejection, and edit controls.
4. An authorized administrator approves the exact draft version.
5. A publishing worker hands the approved draft to the Binance Square adapter.
6. The result and audit event are stored.

## Planned stack

- Python 3.11+
- discord.py
- SQLAlchemy + SQLite
- Pydantic
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
├── commands/
├── core/
├── integrations/binance_square/
├── database/
├── utils/
├── tests/
└── docs/
```

## Setup

1. Install Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and fill in your Discord configuration.
5. Create a Discord application and bot in the Discord Developer Portal; invite it with the required permissions and slash-command scope.
6. Run `python bot.py`.

The initial scaffold will validate configuration and start the Discord client once the bot foundation is implemented.

## Configuration

See `.env.example`. Never commit `.env`, Discord bot tokens, Binance credentials, or user media.

## Security principles

- Default-deny access: only configured submitters may submit drafts.
- Only configured administrators may approve or reject drafts.
- Approval is bound to a draft version; editing invalidates prior approval.
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

- [x] Architecture and initial repository scaffold
- [ ] Discord bot foundation and access control
- [ ] Submission intake and attachment handling
- [ ] Draft preview and approval workflow
- [ ] Persistent database and audit history
- [ ] Binance Square publishing adapter
- [ ] Integration tests and deployment documentation

## License

License to be selected before public release.
