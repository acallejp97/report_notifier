# Report Notifier

A Dockerized Python application that sends automated notifications and reports via a Telegram bot. Scheduled tasks are managed with cron, and process supervision is handled by Supervisor.

## Features

- **Telegram Bot Integration:** Send notifications and reports directly to a Telegram chat.
- **Scheduled Tasks:** Automated report generation and notifications using cron jobs.
- **Dockerized:** Easy deployment and isolation using Docker and Docker Compose.
- **Process Supervision:** Supervisor ensures both the bot and cron jobs run reliably.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Environment Variables

Set the following environment variables in your `docker-compose.yml` or `.env` file:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `TELEGRAM_CHAT_ID`: The chat ID where notifications will be sent.
- `REPORT_TIME`: Time for the daily report (cron format, e.g., `0 8 * * *`).
- `NOTIFY_TIME`: Time for the daily notification (cron format, e.g., `0 9 * * *`).

### Build and Run

```bash
docker-compose up --build
```

### File Structure

```
.
├── app/                  # Application source code
├── saves/                # Generated reports (gitignored)
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
├── supervisord.conf
├── docker-compose.yml
└── README.md
```

## Usage

- The Telegram bot will send notifications and reports at the scheduled times.
- All logs are available in the container logs.

## Development

- Python 3.11 (Alpine)
- Dependencies listed in `requirements.txt`
- You can add unit tests in a `tests/` directory.

## License

MIT License

---

**Author:** Asier Callejo 
**Contact:** asiercallejo20@gmail.com