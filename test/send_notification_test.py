from unittest.mock import Mock

from fruits_and_vegetables_notifier.mailjet_sender import MailJetSender


class SendNotificationTest:
    def setup_method(self):
        self.mailjet_sender = MailJetSender()
        self.mailjet_client = Mock()

    def test_should_send_notification_using_mailjet_client(self):
        # given
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
        self.mailjet_sender.send_notification(self.mailjet_client, notification)

        # then
        self.mailjet_client.send.create.assert_called_once_with(data=notification)

    def test_should_return_true_when_mailjet_client_result_is_ok(self):
        # given
        response = Mock()
        response.ok = True
        self.mailjet_client.send.create.return_value = response

        # when
        result = self.mailjet_sender.send_notification(self.mailjet_client, {})

        # then
        assert result is True

    def test_should_return_false_when_mailjet_client_result_is_not_ok(self):
        # given
        response = Mock()
        response.ok = False
        self.mailjet_client.send.create.return_value = response

        # when
        result = self.mailjet_sender.send_notification(self.mailjet_client, {})

        # then
        assert result is False
