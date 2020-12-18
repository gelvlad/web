from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from webproject.models import Course


class RegisterUserView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)

        user = authenticate(
            username=self.request.POST['username'],
            password=self.request.POST['password1']
        )
        login(self.request, user)

        return response
