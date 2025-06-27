from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, MailingAttempt, Message, Recipient
from .services import send_mailing


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailings:RecipientListView")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise PermissionDenied("Это не ваш клиент.")
        return super().dispatch(request, *args, **kwargs)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailings:RecipientListView")


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailings:RecipientListView")

    def form_valid(self, form_class):
        recipient = form_class.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form_class)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:MessageListView")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого сообщения.")
        return super().dispatch(request, *args, **kwargs)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailings:MessageListView")


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:MessageListView")

    def form_valid(self, form_class):
        message = form_class.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form_class)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:MailingListView")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этой рассылки.")
        if self.object.status != "CREATED":
            raise PermissionDenied(
                "Рассылку можно редактировать только до её отправки."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["message"].queryset = Message.objects.filter(
            owner=self.request.user
        )
        form.fields["recipients"].queryset = Recipient.objects.filter(
            owner=self.request.user
        )
        return form


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailings:MailingListView")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:MailingListView")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["message"].queryset = Message.objects.filter(
            owner=self.request.user
        )
        form.fields["recipients"].queryset = Recipient.objects.filter(
            owner=self.request.user
        )
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = "CREATED"
        return super().form_valid(form)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt


class MailingAttemptDetailView(LoginRequiredMixin, DetailView):
    model = MailingAttempt


def mailingattempt(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)

    if mailing.owner != request.user:
        raise PermissionDenied("Это не ваша рассылка")

    attempt = send_mailing(mailing_id)
    context = {"object": attempt}
    return render(request, "mailings/mailingattempt_detail.html", context)


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "mailings/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        mailings = Mailing.objects.filter(owner=user)
        recipients = Recipient.objects.filter(owner=user)

        context["mailings_count"] = mailings.count()
        context["active_mailings_count"] = mailings.filter(status="STARTED").count()
        context["recipients_count"] = recipients.count()

        return context
