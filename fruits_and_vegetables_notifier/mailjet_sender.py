import os


class MailJetSender:
    def build_notification(self, current_fruits_and_vegetables, next_fruits, next_vegetables):
        fruits_of_month = '<h3>Fruits du mois</h3>' + '<ul><li>' + '</li><li>'.join(
            current_fruits_and_vegetables['fruits']) + '</li></ul>'

        vegetables_of_month = '<h3>Légumes du mois</h3>' + '<ul><li>' + '</li><li>'.join(
            current_fruits_and_vegetables['vegetables']) + '</li></ul>'

        fruits_of_next_month = '<h3>Fruits arrivant le mois prochain</h3>' + '<ul><li>' + '</li><li>'.join(
            next_fruits) + '</li></ul>'

        vegetables_of_next_month = '<h3>Légumes arrivant le mois prochain</h3>' + '<ul><li>' + '</li><li>'.join(
            next_vegetables) + '</li></ul>'

        body = fruits_of_month + fruits_of_next_month + vegetables_of_month + vegetables_of_next_month

        sender_email = os.environ['FROM_EMAIL']
        sender_name = 'Fruits and Vegetables notifier'
        subject = 'Les fruits et légumes du mois ! (et du mois prochain ;))'

        recipients = []
        for recipient in os.environ['TO_EMAILS'].split(','):
            recipients.append({"Email": recipient})

        return {
            'FromEmail': sender_email,
            'FromName': sender_name,
            'Recipients': recipients,
            'Subject': subject,
            'Html-part': body
        }

    def send_notification(self, mailjet_client, notification):
        mailjet_client.send.create(data=notification)
