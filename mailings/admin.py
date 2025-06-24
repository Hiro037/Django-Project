from django.contrib import admin
from.models import Recipient, Message, Mailing, MailingAttempt

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "comment",
        "owner",
    )
    list_filter = (
        "owner",)
    search_fields = (
        "email",
        "full_name",
        "comment",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "owner",
    )
    search_fields = (
        "subject",
        "owner",
    )
    list_filter = (
        "owner",)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "start_time",
        "end_time",
        "status",
        "message",
        "owner",
    )
    search_fields = (
        "status",
        "message",
        "owner",
    )
    list_filter = (
        "owner",
        "status"
    )

@admin.register(MailingAttempt)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "status",
        "mailing",
    )
    search_fields = (
        "status",
        "mailing",
    )
    list_filter = (
        "status",
        "mailing",)