# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class CreateUserForm(UserCreationForm):

#     class Meta:
#         models = User
#         fields = ['username', 'email', 'password1', 'password2']

# Add this to previous list of imports

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'