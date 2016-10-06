import os

from fruits_and_vegetables_notifier.mailjet_sender import MailJetSender


class BuildNotificationTest:
    def setup_method(self):
        self.mailjet_sender = MailJetSender()
        self.current_fruits_and_vegetables = {
            'fruits': [],
            'vegetables': []
        }
        self.next_fruits = []
        self.next_vegetables = []
        os.environ['FROM_EMAIL'] = ''
        os.environ['TO_EMAILS'] = ''

    def test_should_return_dict_using_sender_address_from_os_env(self):
        # given
        os.environ['FROM_EMAIL'] = 'jack.sparrow@blackpearl.org'

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits_and_vegetables, self.next_fruits,
                                                              self.next_vegetables)

        # then
        assert notification['FromEmail'] == 'jack.sparrow@blackpearl.org'

    def test_should_return_dict_with_raw_sender_name(self):
        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits_and_vegetables, self.next_fruits,
                                                              self.next_vegetables)

        # then
        assert notification['FromName'] == 'Fruits and Vegetables notifier'

    def test_should_return_dict_using_recipient_addresses_from_os_env(self):
        # given
        recipient = 'monkey.d.luffy@onepiece.org,roronoa.zoro@onepiece.org'
        os.environ['TO_EMAILS'] = recipient

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits_and_vegetables, self.next_fruits,
                                                              self.next_vegetables)

        # then
        assert len(notification['Recipients']) is 2
        assert notification['Recipients'][0]['Email'] == 'monkey.d.luffy@onepiece.org'
        assert notification['Recipients'][1]['Email'] == 'roronoa.zoro@onepiece.org'

    def test_should_return_dict_with_raw_subject(self):
        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits_and_vegetables, self.next_fruits,
                                                              self.next_vegetables)

        # then
        assert notification['Subject'] == 'Les fruits et légumes du mois ! (et du mois prochain ;))'

    def test_should_return_dict_containing_fruits_of_month_in_html_part(self):
        # given
        self.current_fruits_and_vegetables = {
            'fruits': ['Avocat', 'Raisin'],
            'vegetables': ['Bette', 'Topinambour']
        }

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits_and_vegetables, self.next_fruits,
                                                              self.next_vegetables)

        # then
        assert '<h3>Fruits du mois</h3><ul><li>Avocat</li><li>Raisin</li></ul>' in notification['Html-part']

    def test_should_return_dict_containing_vegetables_of_month_in_html_part(self):
        # given
        self.current_fruits_and_vegetables = {
            'fruits': ['Avocat', 'Raisin'],
            'vegetables': ['Bette', 'Topinambour']
        }

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits_and_vegetables, self.next_fruits,
                                                              self.next_vegetables)

        # then
        assert '<h3>Légumes du mois</h3><ul><li>Bette</li><li>Topinambour</li></ul>' in notification['Html-part']

    def test_should_return_dict_containing_fruits_of_next_month_in_html_part(self):
        # given
        self.next_fruits = ['Kaki', 'Litchi']

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits_and_vegetables, self.next_fruits,
                                                              self.next_vegetables)

        # then
        assert '<h3>Fruits arrivant le mois prochain</h3><ul><li>Kaki</li><li>Litchi</li></ul>' in notification[
            'Html-part']

    def test_should_return_dict_containing_vegetables_of_next_month_in_html_part(self):
        # given
        self.next_vegetables = ['Pomme de terre', 'Potimarron']

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits_and_vegetables, self.next_fruits,
                                                              self.next_vegetables)

        # then
        assert '<h3>Légumes arrivant le mois prochain</h3><ul><li>Pomme de terre</li><li>Potimarron</li></ul>' in \
               notification['Html-part']
