from django.urls import path

from .apps import MailingsConfig
from .views import (HomePageView, MailingAttemptDetailView,
                    MailingAttemptListView, MailingCreateView,
                    MailingDeleteView, MailingDetailView, MailingListView,
                    MailingUpdateView, MessageCreateView, MessageDeleteView,
                    MessageDetailView, MessageListView, MessageUpdateView,
                    RecipientCreateView, RecipientDeleteView,
                    RecipientDetailView, RecipientListView,
                    RecipientUpdateView, mailingattempt)

app_name = MailingsConfig.name

urlpatterns = [
    path("recipients/", RecipientListView.as_view(), name="RecipientListView"),
    path(
        "recipients/detail/<int:pk>/",
        RecipientDetailView.as_view(),
        name="RecipientDetailView",
    ),
    path(
        "recipients/update/<int:pk>/",
        RecipientUpdateView.as_view(),
        name="RecipientUpdateView",
    ),
    path(
        "recipients/delete/<int:pk>/",
        RecipientDeleteView.as_view(),
        name="RecipientDeleteView",
    ),
    path(
        "recipients/create/", RecipientCreateView.as_view(), name="RecipientCreateView"
    ),
    path("messages/", MessageListView.as_view(), name="MessageListView"),
    path(
        "messages/detail/<int:pk>/",
        MessageDetailView.as_view(),
        name="MessageDetailView",
    ),
    path(
        "messages/update/<int:pk>/",
        MessageUpdateView.as_view(),
        name="MessageUpdateView",
    ),
    path(
        "messages/delete/<int:pk>/",
        MessageDeleteView.as_view(),
        name="MessageDeleteView",
    ),
    path("messages/create/", MessageCreateView.as_view(), name="MessageCreateView"),
    path("mailings/", MailingListView.as_view(), name="MailingListView"),
    path(
        "mailings/detail/<int:pk>/",
        MailingDetailView.as_view(),
        name="MailingDetailView",
    ),
    path(
        "mailings/update/<int:pk>/",
        MailingUpdateView.as_view(),
        name="MailingUpdateView",
    ),
    path(
        "mailings/delete/<int:pk>/",
        MailingDeleteView.as_view(),
        name="MailingDeleteView",
    ),
    path("mailings/create/", MailingCreateView.as_view(), name="MailingCreateView"),
    path(
        "mailing-attempts/",
        MailingAttemptListView.as_view(),
        name="MailingAttemptListView",
    ),
    path(
        "mailing-attempts/detail/<int:pk>/",
        MailingAttemptDetailView.as_view(),
        name="MailingAttemptDetailView",
    ),
    path(
        "mailings/detail/<int:mailing_id>/attempt/",
        mailingattempt,
        name="MailingAttempt",
    ),
    path("home/", HomePageView.as_view(), name="HomePage"),
]
