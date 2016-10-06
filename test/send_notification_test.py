from unittest.mock import Mock

from fruits_and_vegetables_notifier.mailjet_sender import MailJetSender


class SendNotificationTest:
    def setup_method(self):
        self.mailjet_sender = MailJetSender()

    def test_should_send_notification_using_mailjet_client(self):
        # given
        mailjet_client = Mock()
        notification = {
            'FromEmail': 'pilot@mailjet.com',
            'FromName': 'Mailjet Pilot',
            'Subject': 'Your email flight plan!',
            'Text-part': 'Dear passenger, welcome to Mailjet! May the delivery force be with you!',
            'Html-part': '<h3>Dear passenger, welcome to Mailjet!</h3><br />May the delivery force be with you!',
            'Recipients': [
                {
                    "Email": "passenger@mailjet.com"
                }
            ]
        }

        # when
        self.mailjet_sender.send_notification(mailjet_client, notification)

        # then
        mailjet_client.send.create.assert_called_once_with(data=notification)
