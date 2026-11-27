# Stage 2 — Multi-Platform Bot Foundation

## Delivered

- Discord client with message-content intent enabled.
- Optional Telegram bot using long polling; Discord remains required.
- Discord application-command synchronization, with `/help` and `/status`.
- Telegram `/start` and `/help` commands.
- Text and supported media intake from both platforms.
- Shared normalized `Submission` object and intake/authorization service used by both adapters.
- Separate platform-specific administrator and submitter allowlists; Telegram IDs are not treated as Discord IDs.
- Default-deny authorization: administrators and explicitly allowlisted submitters only.
- Acknowledgement responses for authorized submissions and rejection notices for unauthorized users.
- Privacy-conscious metadata logging; submitted text/captions and credentials are not logged.
- Graceful shutdown for both clients.

## Telegram setup

1. Create a Telegram bot with [@BotFather](https://t.me/BotFather).
2. Set `TELEGRAM_BOT_TOKEN` in the deployment environment.
3. Set at least one numeric Telegram user ID in `TELEGRAM_ADMIN_USER_IDS`.
4. Optionally set `TELEGRAM_ALLOWED_SUBMITTER_IDS` for additional submitters.
5. Start a private chat with the bot and send `/start`.

Telegram is disabled when `TELEGRAM_BOT_TOKEN` is blank. Discord remains the required platform and continues to use `DISCORD_BOT_TOKEN`, `SUBMISSION_CHANNEL_ID`, and `ADMIN_USER_IDS`.

## Discord Developer Portal setup

1. Create an application and add a bot user.
2. Under **Bot → Privileged Gateway Intents**, enable **Message Content Intent**.
3. Invite the bot with the `bot` and `applications.commands` scopes.
4. Grant only the required permissions: View Channels, Send Messages, Read Message History, and Add Reactions.
5. Set `DISCORD_BOT_TOKEN`, `SUBMISSION_CHANNEL_ID`, and `ADMIN_USER_IDS`.
6. Optionally set `ALLOWED_SUBMITTER_IDS` to allow additional Discord submitters. Empty means only admins can submit.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python bot.py
```

## Stage 2 boundaries

Both adapters pass normalized submission metadata and text/captions into the same intake service. Stage 2 does not persist message content, download/store media, create drafts, approve posts, or publish to Binance. Those features belong to later stages. Attachment counts are recorded; media files are not downloaded.

## Tests

```bash
pytest -q
```
