# Stage 2 — Discord Bot Foundation

## Delivered

- Discord client with message-content intent enabled.
- Application-command synchronization, using a configured guild for fast development sync or global sync otherwise.
- `/help` and `/status` slash commands.
- Default-deny submitter authorization: administrators and explicitly allowlisted submitters only.
- Submission-channel monitoring and acknowledgement reaction for authorized messages.
- Unauthorized submission notices and privacy-conscious event logging (message bodies and credentials are not logged).
- Graceful client shutdown and permission unit tests.

## Discord Developer Portal setup

1. Create an application and add a bot user.
2. Under **Bot → Privileged Gateway Intents**, enable **Message Content Intent**.
3. Invite the bot with the `bot` and `applications.commands` scopes.
4. Grant only the required permissions: View Channels, Send Messages, Read Message History, Add Reactions, and Embed Links.
5. Set `DISCORD_BOT_TOKEN`, `DISCORD_GUILD_ID`, `SUBMISSION_CHANNEL_ID`, and `ADMIN_USER_IDS` in the deployment environment.
6. Optionally set `ALLOWED_SUBMITTER_IDS` to allow additional submitters. Empty means only admins can submit.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python bot.py
```

## Stage 2 boundaries

Submission messages are acknowledged and logged by message ID and attachment count only. Stage 2 does not save message content, download media, create drafts, approve posts, or publish to Binance. Those features belong to later stages.

## Tests

```bash
pytest -q
```
