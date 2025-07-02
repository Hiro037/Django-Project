import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from config.settings import EMAIL_HOST_USER

from .forms import UserRegisterForm
from .models import User


class UserRegisterView(CreateView):
    # Страница регистрации пользователя
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"

        send_mail(
            subject="Подтверждение почты",
            message=f"Чтобы подтвердить адрес электронной почты перейди по этой ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("users.can_see_all_users"):
            raise PermissionDenied("У вас нет прав доступа")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.all()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("users.can_deactivate_users"):
            raise PermissionDenied("У вас нет прав доступа")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.is_active = not self.object.is_active
        self.object.save()

        context = {"object": self.object, "toggled": True}
        return render(request, "users/user_detail.html", context)