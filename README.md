# CryptoWire

A Python Discord-to-Binance Square publishing assistant.

CryptoWire receives content from an authorized Discord server, prepares a draft, and requires an administrator's explicit approval before attempting publication through Binance's official Square publishing integration.

> **Current status:** Discord foundation and administrator-only encrypted API-key setup are implemented. Draft processing, approval, and Binance publishing are not implemented yet.

## Current features

- Discord client and application-command synchronization.
- `/help` and `/status` slash commands.
- Admin-only `/set_api_key` command with a private Discord modal.
- Binance Square API key encrypted at rest using Fernet; the encryption key stays in the host's environment/secrets.
- API-key responses are ephemeral and never echo the submitted key.
- Default-deny submission permissions: administrators and explicitly allowlisted users only.
- Monitoring of one configured submission channel.
- Acknowledgement reaction for authorized submissions.

## Configure encrypted API-key storage

1. Install dependencies: `pip install -r requirements.txt`.
2. Generate an encryption key locally:

   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

3. Set the generated value as `CRYPTOWIRE_SECRET_KEY` in your hosting provider's environment/secrets. Do not commit it.
4. Ensure the bot can write to the configured `BINANCE_SQUARE_SECRET_FILE` path (default: `storage/binance_square_api_key.enc`).
5. Restart the bot and run `/set_api_key` in Discord as a configured administrator.

The bot stores only the encrypted API key on disk. The Fernet encryption key must be backed up securely; if it is lost, the encrypted credential cannot be recovered. Replacing the encryption key requires decrypting and re-encrypting the stored credential first.

**Discord modal limitation:** Discord's modal text input is not a password field, so the value may be visible while the administrator types. The bot does not send it back in a response, log it, or post it to a channel. Use the command only in a trusted Discord environment.

The credential reader is isolated in `integrations/binance_square/credentials.py`; the future Binance publishing adapter should be the only component that calls `load_api_key()`. The command handler has write-only access.

## Setup

1. Install Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and fill in the required Discord configuration and `CRYPTOWIRE_SECRET_KEY`.
5. In the Discord Developer Portal, enable **Message Content Intent** under Bot → Privileged Gateway Intents.
6. Invite the bot with the `bot` and `applications.commands` scopes. Grant only required channel permissions.
7. Run `python bot.py`.

## Required configuration

- `DISCORD_BOT_TOKEN`: bot token from the Discord Developer Portal.
- `SUBMISSION_CHANNEL_ID`: channel where authorized users submit content.
- `ADMIN_USER_IDS`: comma-separated numeric Discord user IDs; at least one is required.
- `CRYPTOWIRE_SECRET_KEY`: Fernet key used to encrypt the API key entered through Discord.

Optional:
- `DISCORD_GUILD_ID`: enables fast guild-scoped slash-command sync during development.
- `ALLOWED_SUBMITTER_IDS`: comma-separated IDs allowed to submit in addition to admins. Empty means admins only.
- `BINANCE_SQUARE_SECRET_FILE`: encrypted credential file path.
- `APPROVAL_CHANNEL_ID`: reserved for the approval workflow stage.

Never commit `.env`, Discord bot tokens, Binance credentials, encryption keys, or user media.

## Security and workflow boundaries

- Only configured administrators can run `/set_api_key`.
- The command response is ephemeral and never displays the credential.
- API keys are encrypted at rest; the encryption key is held separately in the host environment.
- The API-key command can write a credential but cannot read it back.
- Keep the credential reader restricted to the Binance publishing adapter.
- Never publish automatically on receipt; future publishing must require explicit administrator approval.
- Do not grant Binance trading or withdrawal permissions for Square publishing.
- Do not retry ambiguous publishing outcomes blindly; reconcile first to avoid duplicate posts.

## Binance publishing integration

The publishing adapter will be implemented against Binance's official Square publishing integration. Verify current API access, account eligibility, media limits, and credential requirements before enabling production publishing.

- [Official Binance Square publishing integration](https://github.com/binance/binance-skills-hub/tree/main/skills/binance/square-post)
- [Binance Square Creator Center](https://www.binance.com/square/creator-center/home)

## Development status

- [x] Stage 1: architecture and repository scaffold
- [x] Stage 2: Discord bot foundation and access control
- [x] Admin-only encrypted Binance API-key configuration
- [ ] Stage 3: submission intake, attachment handling, and drafts
- [ ] Stage 4: approval workflow
- [ ] Stage 5: Binance Square publishing adapter
- [ ] Stage 6: persistent database and audit history
- [ ] Stage 7: integration tests and deployment

## Tests

```bash
pytest -q
```
