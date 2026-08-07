# my-booker-buddy

Automated Selenium bot that books padel courts on [Padel7](https://padel7santmarti.com) (Barcelona). Supports multiple venues, court type preferences, dry-run mode, scheduled execution, and Slack notifications.

## Supported venues

| Key | Location |
|-----|----------|
| `poblenou` | Padel7 Poblenou (default) |
| `glories` | Padel7 Glòries |

## Setup

**Requirements:** Python 3.12+, [uv](https://github.com/astral-sh/uv)

```bash
cd padel7_booking_bot
uv sync
```

Create a `.env` file in `padel7_booking_bot/`:

```
APP_USERNAME=your@email.com
APP_PASSWORD=yourpassword
APP_SLACK_TOKEN=xoxb-...          # optional
APP_SLACK_PROD_WEBHOOK_URL=https://hooks.slack.com/...   # optional
APP_SLACK_TEST_WEBHOOK_URL=https://hooks.slack.com/...   # optional
```

## Usage

```bash
uv run python main.py [OPTIONS]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` / `--no-dry-run` | `--dry-run` | Simulate without spending money. Pass `--no-dry-run` for a real booking. |
| `--date YYYY-MM-DD` | 10 days from now | Date to book |
| `--time HH:MM` | `18:00-19:30` | Time slot to book |
| `--court-type` | `both` | `indoor`, `outdoor`, or `both` |
| `--centre` | `poblenou` | `poblenou` or `glories` |
| `--wait-until HH:MM:SS` | — | Wait until this exact time (Europe/Madrid) before running — useful when bookings open at midnight |
| `--notifications` | off | Send Slack notification on result |
| `--verbose` | off | Enable debug logging |

### Examples

```bash
# Dry run (safe, default) — test the flow without booking
uv run python main.py --date 2026-08-17 --time 18:00

# Real booking at Poblenou
uv run python main.py --no-dry-run --date 2026-08-17 --time 18:00 --centre poblenou

# Wait until midnight then book (new-day reservations)
uv run python main.py --no-dry-run --wait-until 00:00:00 --date 2026-08-18 --time 10:00

# Book an indoor court at Glòries with Slack notification
uv run python main.py --no-dry-run --date 2026-08-17 --time 18:00 --centre glories --court-type indoor --notifications
```

## Docker

```bash
cd padel7_booking_bot
bash build_image.sh

docker run --rm \
  --env-file .env \
  padel7-booking-bot:0.0.1 \
  --no-dry-run --date 2026-08-17 --time 18:00 --centre poblenou
```

The Docker image runs Chrome in headless mode automatically (`ENV=docker`).

## Output

- **Screenshots** saved to `padel7_booking_bot/screenshots/` after each run
- **Logs** written to `padel7_booking_bot/logs/bot.log`
- **Slack notification** sent on success or failure (if `--notifications` is set)

## Running tests

```bash
cd padel7_booking_bot
uv run pytest
```
