import os


class MailJetSender:
    def build_notification(self, current_fruits, current_vegetables, next_fruits, next_vegetables):
        body = self.__build_notification_body(
            current_fruits,
            current_vegetables,
            next_fruits,
            next_vegetables)

        sender_email = os.environ['FROM_EMAIL']
        sender_name = 'Fruits et légumes du mois'
        subject = 'Les %d fruits et %d légumes du mois ! (et ceux arrivant le mois prochain)' \
                  % (len(current_fruits), len(current_vegetables))

        recipients = []
        for recipient in os.environ['TO_EMAILS'].split(','):
            recipients.append({"Email": recipient})

        notification = {
            'FromEmail': sender_email,
            'FromName': sender_name,
            'Recipients': recipients,
            'Subject': subject,
            'Html-part': body
        }

        reply_to_environment_variable = 'REPLY_TO'
        if reply_to_environment_variable in os.environ:
            notification.update({'Headers': {'Reply-To': os.environ[reply_to_environment_variable]}})

        return notification

    def send_notification(self, mailjet_client, notification):
        result = mailjet_client.send.create(data=notification)
        return result.ok

    def __build_notification_body(self, current_fruits, current_vegetables, next_fruits, next_vegetables):
        notification_template = \
            '<h3>{title}</h3>' + \
            '<ul>' + \
            '<li>{elements}</li>' + \
            '</ul>'

        body = ''
        for title, elements in [
            ('Fruits du mois', current_fruits),
            ('Légumes du mois', current_vegetables),
            ('Fruits arrivant le mois prochain', next_fruits),
            ('Légumes arrivant le mois prochain', next_vegetables)
        ]:
            if elements:
                body += notification_template.format(title=title, elements='</li><li>'.join(sorted(elements)))

        signature = '<br/><small><i>Fruits and vegetables notifier, an open-source software available on <a href="https://github.com/damienbeaufils/fruits-and-vegetables-notifier">GitHub</a>' + \
                    '<br/>Data kindly provided by https://www.fruits-legumes.org/</i></small>'
        return body + signature
