import requests
import json
import logging


def send_booking_notification(
    webhook_url, token, booking_details, booking_successful=True
):
    """
    Send a booking notification to Slack.
    Args:
        webhook_url (str): The Slack webhook URL.
        token (str): The Slack token for authentication.
        booking_details (dict): A dictionary containing booking details.
        booking_successful (bool): Indicates if the booking was successful. Default is True.
    """
    # Check if the booking was successful
    if booking_successful is False:
        # If booking was not successful, create a failure message
        logging.debug("Booking was not successful.")
        # Create the payload for the Slack message
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":redalert:  There was a problem booking a court! :redalert: ",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*📅 Date:*\n*{booking_details['date']}*",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*⏰ Time:*\n*{booking_details['time']}*",
                        },
                    ],
                },
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": " ", "emoji": True},
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*🏟️ Court:*\n*{booking_details['court']}*",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*📍 Location:*\n*{booking_details['location']}*",
                        },
                    ],
                },
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": " ", "emoji": True},
                },
                {"type": "divider"},
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Please check the booking system for more details.",
                        }
                    ],
                },
            ]
        }

    else:
        # If booking was successful, create a success message
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🎾 COURT BOOKED! TIME TO SLAY! 🎉",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*📅 Date:*\n*{booking_details['date']}*",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*⏰ Time:*\n*{booking_details['time']}*",
                        },
                    ],
                },
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": " ", "emoji": True},
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*🏟️ Court:*\n*{booking_details['court']}*",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*📍 Location:*\n*{booking_details['location']}*",
                        },
                    ],
                },
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": " ", "emoji": True},
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*💸 Cost:*\n*{booking_details['cost']} (Split it, no excuses! 😜)*",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*:man-raising-hand: Booked by:*\n*{booking_details['booked_by']}*",
                        },
                    ],
                },
                {"type": "divider"},
                {
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": "💪 *LET’S MAKE IT EPIC!* 🎯"}
                    ],
                },
            ]
        }

    logging.debug(f"payload : {payload}")

    # Send the payload to the Slack webhook
    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    # Check the response from the server
    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )
    else:
        logging.info("Notification sent successfully.")
