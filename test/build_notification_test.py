import os

from fruits_and_vegetables_notifier.mailjet_sender import MailJetSender


class BuildNotificationTest:
    def setup_method(self):
        self.mailjet_sender = MailJetSender()
        self.current_fruits = {}
        self.current_vegetables = {}
        self.next_fruits = {}
        self.next_vegetables = {}

        os.environ.clear()
        os.environ['FROM_EMAIL'] = ''
        os.environ['TO_EMAILS'] = ''

    def test_should_return_dict_using_sender_address_from_os_env(self):
        # given
        os.environ['FROM_EMAIL'] = 'jack.sparrow@blackpearl.org'

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert notification['FromEmail'] == 'jack.sparrow@blackpearl.org'

    def test_should_return_dict_with_raw_sender_name(self):
        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert notification['FromName'] == 'Fruits et légumes du mois'

    def test_should_return_dict_using_recipient_addresses_from_os_env(self):
        # given
        recipient = 'monkey.d.luffy@onepiece.org,roronoa.zoro@onepiece.org'
        os.environ['TO_EMAILS'] = recipient

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert len(notification['Recipients']) is 2
        assert notification['Recipients'][0]['Email'] == 'monkey.d.luffy@onepiece.org'
        assert notification['Recipients'][1]['Email'] == 'roronoa.zoro@onepiece.org'

    def test_should_return_dict_with_subject_containing_number_of_fruits_and_vegetables(self):
        # given
        self.current_fruits = {'Avocat', 'Raisin', 'Mandarine'}
        self.current_vegetables = {'Bette', 'Topinambour'}

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert notification['Subject'] == 'Les 3 fruits et 2 légumes du mois ! (et ceux arrivant le mois prochain)'

    def test_should_return_dict_containing_fruits_of_month_in_html_part(self):
        # given
        self.current_fruits = {'Avocat', 'Raisin'}
        self.current_vegetables = {'Bette', 'Topinambour'}

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert '<h3>Fruits du mois</h3><ul><li>Avocat</li><li>Raisin</li></ul>' in notification['Html-part']

    def test_should_return_dict_containing_vegetables_of_month_in_html_part(self):
        # given
        self.current_fruits = {'Avocat', 'Raisin'}
        self.current_vegetables = {'Bette', 'Topinambour'}

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert '<h3>Légumes du mois</h3><ul><li>Bette</li><li>Topinambour</li></ul>' in notification['Html-part']

    def test_should_return_dict_containing_fruits_of_next_month_in_html_part(self):
        # given
        self.next_fruits = {'Kaki', 'Litchi'}

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert '<h3>Fruits arrivant le mois prochain</h3><ul><li>Kaki</li><li>Litchi</li></ul>' in notification[
            'Html-part']

    def test_should_return_dict_containing_vegetables_of_next_month_in_html_part(self):
        # given
        self.next_vegetables = {'Pomme de terre', 'Potimarron'}

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert '<h3>Légumes arrivant le mois prochain</h3><ul><li>Pomme de terre</li><li>Potimarron</li></ul>' in \
               notification['Html-part']

    def test_should_return_dict_containing_signature_in_html_part(self):
        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert notification['Html-part'].endswith(
            '<br/><small><i>Fruits and vegetables notifier, an open-source software available on <a href="https://github.com/damienbeaufils/fruits-and-vegetables-notifier">GitHub</a>' + \
            '<br/>Data kindly provided by https://www.fruits-legumes.org/</i></small>')

    def test_should_add_reply_to_header_when_existing_in_environment_variable(self):
        # given
        os.environ['REPLY_TO'] = 'tony@stackindustries.com'

        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)

        # then
        assert notification['Headers'] == {'Reply-To': 'tony@stackindustries.com'}

    def test_should_not_add_any_header_when_no_reply_to_environment_variable(self):
        # when
        notification = self.mailjet_sender.build_notification(self.current_fruits, self.current_vegetables,
                                                              self.next_fruits, self.next_vegetables)
        # then
        assert 'Headers' not in notification
