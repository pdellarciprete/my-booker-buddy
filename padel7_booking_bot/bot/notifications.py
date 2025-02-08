import requests
import json
import logging


def send_booking_notification(webhook_url, token, booking_details):
    # Create the payload for the Slack message
    payload = {
        "blocks": [
          {
            "type": "header",
            "text": {
              "type": "plain_text",
              "text": "🎾 COURT BOOKED! TIME TO SLAY! 🎉",
              "emoji": True
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "fields": [
              {
                "type": "mrkdwn",
                "text": f"*📅 Date:*\n*{booking_details['date']}*"
              },
              {
                "type": "mrkdwn",
                "text": f"*⏰ Time:*\n*{booking_details['time']}*"
              }
            ]
          },
          {
            "type": "section",
            "text": {
              "type": "plain_text",
              "text": " ",
              "emoji": True
            }
          },
          {
            "type": "section",
            "fields": [
              {
                "type": "mrkdwn",
                "text": f"*🏟️ Court:*\n*{booking_details['court']}*"
              },
              {
                "type": "mrkdwn",
                "text": f"*📍 Location:*\n*{booking_details['location']}*"
              }
            ]
          },
          {
            "type": "section",
            "text": {
              "type": "plain_text",
              "text": " ",
              "emoji": True
            }
          },
          {
            "type": "section",
            "fields": [
              {
                "type": "mrkdwn",
                "text": f"*💸 Cost:*\n*{booking_details['cost']} (Split it, no excuses! 😜)*"
              }
            ]
          },
          {
            "type": "divider"
          },
          {
            "type": "context",
            "elements": [
              {
                "type": "mrkdwn",
                "text": "💪 *LET’S MAKE IT EPIC!* 🎯"
              }
            ]
          }
        ]
    }

    logging.debug(f"payload : {payload}")

    # Send the payload to the Slack webhook
    response = requests.post(
        webhook_url, data=json.dumps(payload),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )

    # Check the response from the server
    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )
    else:
        logging.info("Notification sent successfully.")


