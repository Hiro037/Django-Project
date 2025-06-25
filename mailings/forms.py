from django.forms import ModelForm
from .models import Recipient,Message, Mailing

class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'recipients']

