import unittest
import json
import os
from config import settings
from bot import notifications
from unittest.mock import patch, Mock

from dotenv import load_dotenv

class TestSendSlackNotification(unittest.TestCase):

    @patch('bot.notifications.requests.post')
    def test_send_slack_notification_success(self, mock_post):

        load_dotenv()

        # Personal chat with Pier
        webhook_url = settings.SLACK_TEST_WEBHOOK_URL
        token = os.getenv("APP_SLACK_TOKEN")
        booking_details = {
            "date": "February 18th, 2025",
            "time": "6:00 PM - 7:30 PM",
            "court": "Indoor 1",
            "location": "Padel7 Glories, Barcelona",
            "cost": "€48"
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Act
        notifications.send_booking_notification(webhook_url, token, booking_details)

        # Assert
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args[1]['headers']['Authorization'], f'Bearer {token}')
        self.assertEqual(json.loads(mock_post.call_args[1]['data'])['blocks'][2]['fields'][0]['text'], f"*📅 Date:*\n*{booking_details['date']}*")
        self.assertEqual(json.loads(mock_post.call_args[1]['data'])['blocks'][2]['fields'][1]['text'], f"*⏰ Time:*\n*{booking_details['time']}*")
        self.assertEqual(json.loads(mock_post.call_args[1]['data'])['blocks'][4]['fields'][0]['text'], f"*🏟️ Court:*\n*{booking_details['court']}*")
        self.assertEqual(json.loads(mock_post.call_args[1]['data'])['blocks'][4]['fields'][1]['text'], f"*📍 Location:*\n*{booking_details['location']}*")
        self.assertEqual(json.loads(mock_post.call_args[1]['data'])['blocks'][6]['fields'][0]['text'], f"*💸 Cost:*\n*{booking_details['cost']} (Split it, no excuses! 😜)*")
        print("Test for successful notification passed.")

    @patch('bot.notifications.requests.post')
    def test_send_slack_notification_failure(self, mock_post):

        load_dotenv()

        # Personal chat with Pier
        webhook_url = settings.SLACK_TEST_WEBHOOK_URL
        token = os.getenv("APP_SLACK_TOKEN")
        booking_details = {
            "date": "February 18th, 2025",
            "time": "6:00 PM - 7:30 PM",
            "court": "Indoor 1",
            "location": "Padel7 Glories, Barcelona",
            "cost": "€48"
        }
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            notifications.send_booking_notification(webhook_url, token, booking_details)

        self.assertIn("Request to Slack returned an error 400", str(context.exception))
        print("Test for failed notification passed.")

if __name__ == '__main__':
    unittest.main()