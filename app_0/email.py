import threading

from django.core.mail import EmailMultiAlternatives


def send_simple_message(subject, body, from_mail, recipient_list, html=None, attachment=None):
    """
    Email sending with text and template in the body.
    """
    subject, from_email, to = subject, from_mail, recipient_list
    text_content = body
    html_content = html
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    if html:
        msg.attach_alternative(html_content, "text/html")
    msg.content_subtype = "html"
    if attachment:
        msg.attach('file.pdf', attachment, 'application/pdf')
    msg.send()


class EmailThread(threading.Thread):

    def __init__(self, subject, body, from_email, recipient_list,
                 fail_silently, html, attachment):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        self.attachment = attachment
        threading.Thread.__init__(self)

    def run(self):
        if self.html is None:
            send_simple_message(self.subject, self.body, self.from_email,
                                self.recipient_list)
        else:
            send_simple_message(self.subject, self.body, self.from_email,
                                self.recipient_list, html=self.html, attachment=self.attachment)


def thread_mail(subject, body, from_email, recipient_list,
                fail_silently=False, html=None, attachment=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently,
                html, attachment).start()
