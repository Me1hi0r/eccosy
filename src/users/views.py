from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ChangeUser(generic.UpdateView):
    model = User
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('order:list')
    template_name = 'registration/change.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)
