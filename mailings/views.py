from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, MailingAttempt, Message, Recipient
from .services import send_mailing


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.has_perm("can_view_all_recipients"):
            context["object_list"] = Recipient.objects.all()
        else:
            context["object_list"] = Recipient.objects.filter(owner=user)
        return context


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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.has_perm("can_view_all_messages"):
            context["object_list"] = Message.objects.all()
        else:
            context["object_list"] = Message.objects.filter(owner=user)
        return context


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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.has_perm("can_view_all_mailings"):
            context["object_list"] = Mailing.objects.all()
        else:
            context["object_list"] = Mailing.objects.filter(owner=user)
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Только владелец или менеджер может менять статус активности
        is_owner = self.object.owner == request.user
        is_manager = request.user.has_perm("mailings.can_disable_mailings")

        if not (is_owner or is_manager):
            raise PermissionDenied("Вы не можете изменить состояние этой рассылки.")

        self.object.is_active = not self.object.is_active
        self.object.save()

        context = {"object": self.object, "toggled": True}
        return render(request, "mailings/mailing_detail.html", context)


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


@method_decorator(cache_page(60 * 5), name="dispatch")
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "mailings/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        last_month = timezone.now() - timedelta(days=30)

        mailings = Mailing.objects.filter(owner=user)
        recipients = Recipient.objects.filter(owner=user)
        mailing_attempts = MailingAttempt.objects.filter(
            mailing__in=mailings, timestamp__gte=last_month  # попытки не старше 30 дней
        )
        success_mailing_attempts = mailing_attempts.filter(status="SUCCESS")
        failure_mailing_attempts = mailing_attempts.filter(status="FAILURE")
        sent_emails = (
            success_mailing_attempts.aggregate(Sum("emails_sent"))["emails_sent__sum"]
            or 0
        )

        context["mailings_count"] = mailings.count()
        context["active_mailings_count"] = mailings.filter(status="STARTED").count()
        context["recipients_count"] = recipients.count()
        context["mailing_attempts"] = mailing_attempts.count()
        context["success_mailing_attempts"] = success_mailing_attempts.count()
        context["failure_mailing_attempts"] = failure_mailing_attempts.count()
        context["sent_emails"] = sent_emails

        return context
