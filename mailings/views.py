from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .models import Recipient, Message, Mailing, MailingAttempt

# from .forms import RecipientForm

class RecipientListView(ListView):
    model = Recipient

class RecipientDetailView(DetailView):
    model = Recipient

class RecipientUpdateView(UpdateView):
    model = Recipient
    pass
    # form_class = RecipientForm
    #
    # def get_form_class(self):
    #     user = self.request.user
    #     if user == self.object.owner:
    #         return RecipientForm
    #     return PermissionError

class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy('mailings:RecipientListVew')

class RecipientCreateView(CreateView):
    model = Recipient
    pass
    # form_class = RecipientForm
    #
    # def form_valid(self, form_class):
    #     recipient = form_class.save()
    #     user = self.request.user
    #     recipient.owner = user
    #     recipient.save()
    #     return super().form_valid(form_class)

class MessageListView(ListView):
    model = Message
    pass

class MessageDetailView(DetailView):
    model = Message
    pass

class MessageUpdateView(UpdateView):
    model = Message
    pass

class MessageDeleteView(DeleteView):
    model = Message
    pass

class MessageCreateView(CreateView):
    model = Message
    pass

class MailingListView(ListView):
    model = Mailing
    pass

class MailingDetailView(DetailView):
    model = Mailing
    pass

class MailingUpdateView(UpdateView):
    model = Mailing
    pass

class MailingDeleteView(DeleteView):
    model = Mailing
    pass

class MailingCreateView(CreateView):
    model = Mailing
    pass

class MailingAttemptListView(ListView):
    model = MailingAttempt
    pass

class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    pass

class MailingAttemptUpdateView(UpdateView):
    model = MailingAttempt
    pass

class MailingAttemptDeleteView(DeleteView):
    model = MailingAttempt
    pass

class MailingAttemptCreateView(CreateView):
    model = MailingAttempt
    pass