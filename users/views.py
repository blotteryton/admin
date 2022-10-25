from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from users.forms import UserCreationForm
from users.models import User, NFT

class Register(View):

    template_name = 'register.html'

    def get(self, request):
        context = {
          'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #get user
            user = authenticate(username=username, password=password)
            #set user group
            bloggers_group = Group.objects.get(name='bloggers')
            bloggers_group.user_set.add(user)
            #set access to admin panel
            user.is_staff = True
            user.save()
            #redirect to admin panel
            return redirect('../login/')
        else:
            context = {
                "form": form
            }
            return render(request, self.template_name, context)
