import os
from unittest.mock import Mock

from fruits_and_vegetables_notifier.crawler import Crawler
from fruits_and_vegetables_notifier.mailjet_sender import MailJetSender
from run import main


class MainTest:
    def setup_method(self):
        self.current_month = 12
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
        self.api_key = 'mailjet_api_public_key'
        self.api_secret = 'mailjet_api_private_key'

        os.environ.clear()
        os.environ['MJ_APIKEY_PUBLIC'] = self.api_key
        os.environ['MJ_APIKEY_PRIVATE'] = self.api_secret

    def test_should_send_cron_notification_containing_current_and_next_crawled_fruits_and_vegetables(self):
        # given
        crawler = Crawler()
        crawler.get_fruits_and_vegetables_of_month = Mock(side_effect=self.__get_fruits_and_vegetables_of_month_stub)

        mailjet_sender = MailJetSender()
        mailjet_sender.build_notification = Mock(side_effect=self.__build_notification_stub)
        mailjet_sender.send_notification = Mock()

        os.environ['TRAVIS_EVENT_TYPE'] = 'cron'

        # when
        main(crawler, mailjet_sender, self.current_month)

        # then
        match_mailjet_client = MailJetClientMatcher((self.api_key, self.api_secret))
        mailjet_sender.send_notification.assert_called_once_with(match_mailjet_client, self.notification)

    def test_should_not_send_any_notification_when_script_is_not_launched_by_a_cron_job(self):
        # given
        crawler = Crawler()
        crawler.get_fruits_and_vegetables_of_month = Mock(side_effect=self.__get_fruits_and_vegetables_of_month_stub)

        mailjet_sender = MailJetSender()
        mailjet_sender.build_notification = Mock(side_effect=self.__build_notification_stub)
        mailjet_sender.send_notification = Mock()

        os.environ['TRAVIS_EVENT_TYPE'] = 'push'

        # when
        main(crawler, mailjet_sender, self.current_month)

        # then
        assert mailjet_sender.send_notification.call_count == 0

    def __get_fruits_and_vegetables_of_month_stub(self, month):
        if month == self.current_month:
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
