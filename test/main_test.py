import os
from unittest.mock import Mock

from fruits_and_vegetables_notifier.crawler import Crawler
from fruits_and_vegetables_notifier.mailjet_sender import MailJetSender
from run import main


class MainTest:
    def setup_method(self):
        self.current_month_fruits_and_vegetables = {
            'fruits': {'Banane'},
            'vegetables': {'Asperge'}
        }
        self.next_month_fruits_and_vegetables = {
            'fruits': {'Banane', 'Kiwi'},
            'vegetables': {'Asperge', 'Carotte'}
        }
        self.notification = {
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

    def test_should_send_notification_containing_current_and_next_crawled_fruits_and_vegetables(self):
        # given
        current_month = 12

        crawler = Crawler()
        crawler.get_fruits_and_vegetables_of_month = Mock(side_effect=self.__get_fruits_and_vegetables_of_month_stub)

        mailjet_sender = MailJetSender()
        mailjet_sender.build_notification = Mock(side_effect=self.__build_notification_stub)
        mailjet_sender.send_notification = Mock()

        api_key = 'mailjet_api_public_key'
        api_secret = 'mailjet_api_private_key'
        os.environ['MJ_APIKEY_PUBLIC'] = api_key
        os.environ['MJ_APIKEY_PRIVATE'] = api_secret

        # when
        main(crawler, mailjet_sender, current_month)

        # then
        match_mailjet_client = MailJetClientMatcher((api_key, api_secret))
        mailjet_sender.send_notification.assert_called_once_with(match_mailjet_client, self.notification)

    def __get_fruits_and_vegetables_of_month_stub(self, month):
        if month == 12:
            return self.current_month_fruits_and_vegetables
        elif month == 1:
            return self.next_month_fruits_and_vegetables
        else:
            raise ValueError()

    def __build_notification_stub(self, current_fruits, current_vegetables, next_fruits, next_vegetables):
        if (current_fruits == {'Banane'} and current_vegetables == {'Asperge'}
            and next_fruits == {'Kiwi'} and next_vegetables == {'Carotte'}):
            return self.notification
        else:
            raise ValueError()


class MailJetClientMatcher:
    def __init__(self, auth):
        self.auth = auth

    def __eq__(self, other):
        return self.auth == other.auth
