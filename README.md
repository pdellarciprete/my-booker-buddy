# my-booker-buddy

Automated Selenium bot that books padel courts on [Padel7](https://padel7santmarti.com) (Barcelona). Supports multiple venues, court type preferences with automatic fallback, dry-run mode, scheduled execution, and Slack notifications.

## Supported Venues

| Key | Location |
|-----|----------|
| `poblenou` | Padel7 Poblenou (default) |
| `glories` | Padel7 Glòries |

## Project Structure

```text
my-booker-buddy/
├── README.md                  # Project documentation
├── Taskfile.yml               # Task runner shortcuts for local and Docker workflows
└── padel7_booking_bot/
    ├── pyproject.toml         # Project metadata and dependencies (managed with uv)
    ├── uv.lock                # Locked dependency versions
    ├── Dockerfile             # Container definition with headless Chrome
    ├── .env                   # Local credentials and Slack webhooks (git-ignored)
    ├── main.py                # CLI entry point and workflow orchestration
    ├── config/
    │   └── settings.py        # Venue URLs, court mappings, timeouts, and directories
    ├── bot/
    │   ├── login.py           # Cookie handling and member portal authentication
    │   ├── booking.py         # Date navigation, slot lookup, and checkout flow
    │   ├── utils.py           # Chrome driver setup, court selection, logging, screenshots
    │   └── types.py           # TypedDict definitions for booking state and preferences
    ├── logs/                  # Execution logs (bot.log)
    ├── screenshots/           # Final-state screenshots saved after each run
    └── tests/                 # Unit and integration test suites
```

## Setup

**Requirements:** Python 3.12+, [uv](https://github.com/astral-sh/uv), [Task](https://taskfile.dev) (recommended)

From the repository root:

```bash
task setup
```

*(Without `task`, run `cd padel7_booking_bot && mkdir -p screenshots logs && uv sync`.)*

Create a `.env` file inside `padel7_booking_bot/`:

```env
APP_USERNAME=your@email.com
APP_PASSWORD=yourpassword
APP_SLACK_TOKEN=xoxb-...                                 # optional
APP_SLACK_PROD_WEBHOOK_URL=[https://hooks.slack.com/](https://hooks.slack.com/)...   # optional
APP_SLACK_TEST_WEBHOOK_URL=[https://hooks.slack.com/](https://hooks.slack.com/)...   # optional
```

## Usage

Run tasks from the repository root (pass any CLI flags after `--`), or invoke `uv run python main.py` directly inside `padel7_booking_bot/`:

```bash
task dry-run -- [OPTIONS]
task run -- [OPTIONS]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` / `--no-dry-run` | `--dry-run` | Simulate without spending balance. `task run` passes `--no-dry-run` automatically. |
| `--date YYYY-MM-DD` | 10 days from now | Target booking date |
| `--time HH:MM` | `18:00-19:30` | Time slot to book |
| `--court-type` | `both` | `indoor`, `outdoor`, or `both` (falls back to any available court if preferred type is full) |
| `--centre` | `poblenou` | `poblenou` or `glories` |
| `--wait-until HH:MM:SS` | — | Wait until this exact time (`Europe/Madrid`) before running — useful for midnight booking drops |
| `--notifications` | off | Send Slack notification on booking result |
| `--verbose` | off | Enable debug logging |

### Examples

```bash
# Dry run (safe default) — test the booking flow without paying
task dry-run --date 2026-08-17 --time 18:00

# Real booking at Poblenou
task run --date 2026-08-17 --time 18:00 --centre poblenou

# Wait until midnight then book immediately when new slots open
task run --wait-until 00:00:00 --date 2026-08-18 --time 10:00

# Book an indoor court at Glòries with Slack notifications enabled
task run --date 2026-08-17 --time 18:00 --centre glories --court-type indoor --notifications
```

## Docker

Build the container image:

```bash
task docker:build
```

Run a dry-run test or live booking in Docker (automatically loads `.env` and mounts `screenshots/` and `logs/` to your host):

```bash
# Dry run with debug logging
task docker:dry-run --verbose

# Live booking
task docker:run --date 2026-08-17 --time 18:00 --centre poblenou
```

The container runs Chrome in headless mode automatically (`ENV=docker`).

## Workflow & Output

1. **Login:** Authenticates against the Padel7 portal via `bot/login.py`.
2. **Court Selection:** Finds matching time slots via `bot/booking.py` and selects the best court (`bot/utils.py`), falling back to any court type if your `--court-type` preference is unavailable.
3. **Checkout & Artifacts:**
   - **Screenshots** saved to `padel7_booking_bot/screenshots/` after each run (useful for inspecting errors or dry-run states).
   - **Logs** written to `padel7_booking_bot/logs/bot.log`.
   - **Slack notifications** dispatched on success or failure when `--notifications` is passed.

## Testing & Maintenance

```bash
# Run the pytest suite
task test

# Clear saved screenshots and log files
task clean
```