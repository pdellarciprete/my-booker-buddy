import requests
import json
import logging

from bot.types import BookingDetails


def _booking_info_blocks(booking_details: BookingDetails) -> list:
    return [
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*📅 Date:*\n*{booking_details['date']}*"},
                {"type": "mrkdwn", "text": f"*⏰ Time:*\n*{booking_details['time']}*"},
            ],
        },
        {"type": "section", "text": {"type": "plain_text", "text": " ", "emoji": True}},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*🏟️ Court:*\n*{booking_details['court']}*"},
                {"type": "mrkdwn", "text": f"*📍 Location:*\n*{booking_details['location']}*"},
            ],
        },
        {"type": "section", "text": {"type": "plain_text", "text": " ", "emoji": True}},
    ]


def _build_success_payload(booking_details: BookingDetails) -> dict:
    return {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🎾 COURT BOOKED! TIME TO SLAY! 🎉", "emoji": True},
            },
            *_booking_info_blocks(booking_details),
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*💸 Cost:*\n*{booking_details['cost']} (Split it, no excuses! 😜)*"},
                    {"type": "mrkdwn", "text": f"*:man-raising-hand: Booked by:*\n*{booking_details['booked_by']}*"},
                ],
            },
            {"type": "divider"},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": "💪 *LET'S MAKE IT EPIC!* 🎯"}]},
        ]
    }


def _build_failure_payload(booking_details: BookingDetails) -> dict:
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":redalert:  There was a problem booking a court! :redalert: ",
                    "emoji": True,
                },
            },
            *_booking_info_blocks(booking_details),
            {"type": "divider"},
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": "Please check the booking system for more details."}],
            },
        ]
    }


def send_booking_notification(
    webhook_url: str,
    token: str,
    booking_details: BookingDetails,
    booking_successful: bool = True,
) -> None:
    payload = _build_success_payload(booking_details) if booking_successful else _build_failure_payload(booking_details)
    logging.debug("payload: %s", payload)

    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )
    logging.info("Notification sent successfully.")
